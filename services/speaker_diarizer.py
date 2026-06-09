"""
Speaker diarization menggunakan Pyannote Audio.
Menambahkan label speaker ke setiap segmen transkrip.
"""
import subprocess
from pathlib import Path

from config_ican import HUGGINGFACE_TOKEN, TEMP_DIR


class SpeakerDiarizer:
    """Identifikasi siapa berbicara di setiap segmen audio."""

    def __init__(self, hf_token=None):
        self.hf_token = hf_token or HUGGINGFACE_TOKEN
        self._pipeline = None

    def _load_pipeline(self):
        if self._pipeline is not None:
            return self._pipeline

        if not self.hf_token:
            print("⚠️  HUGGINGFACE_TOKEN tidak diset — skip diarization")
            return None

        try:
            from pyannote.audio import Pipeline
            import torch

            print("🎙️  Loading Pyannote speaker-diarization-3.1...")
            try:
                self._pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    token=self.hf_token,
                )
            except TypeError:
                self._pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=self.hf_token,
                )
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self._pipeline.to(device)
            print(f"✅ Pyannote loaded on {device}")
            return self._pipeline
        except Exception as e:
            print(f"⚠️  Pyannote gagal dimuat: {e}")
            return None

    def _extract_audio(self, video_path):
        """Ekstrak audio WAV mono 16kHz untuk Pyannote."""
        audio_path = TEMP_DIR / f"{Path(video_path).stem}_diarize.wav"
        cmd = [
            "ffmpeg", "-y", "-i", str(video_path),
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
            str(audio_path),
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        return audio_path

    def diarize(self, video_path):
        """
        Jalankan diarization pada video.

        Returns:
            list[dict]: [{'start': float, 'end': float, 'speaker': str}, ...]
        """
        pipeline = self._load_pipeline()
        if pipeline is None:
            return []

        try:
            audio_path = self._extract_audio(video_path)
            print("🎙️  Menjalankan speaker diarization...")

            diarization = pipeline(str(audio_path))
            turns = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                turns.append({
                    'start': turn.start,
                    'end': turn.end,
                    'speaker': speaker,
                })

            print(f"✅ Diarization selesai: {len(turns)} speaker turns")
            if audio_path.exists():
                audio_path.unlink()
            return turns

        except Exception as e:
            print(f"⚠️  Diarization gagal: {e}")
            return []

    @staticmethod
    def assign_speakers_to_segments(segments, speaker_turns):
        """Gabungkan label speaker ke segmen Whisper berdasarkan overlap waktu."""
        if not speaker_turns:
            for seg in segments:
                seg['speaker'] = 'SPEAKER_00'
            return segments

        for seg in segments:
            best_speaker = 'SPEAKER_00'
            best_overlap = 0.0
            seg_mid = (seg['start'] + seg['end']) / 2

            for turn in speaker_turns:
                if turn['start'] <= seg_mid <= turn['end']:
                    overlap = min(seg['end'], turn['end']) - max(seg['start'], turn['start'])
                    if overlap > best_overlap:
                        best_overlap = overlap
                        best_speaker = turn['speaker']

            seg['speaker'] = best_speaker

        return segments
