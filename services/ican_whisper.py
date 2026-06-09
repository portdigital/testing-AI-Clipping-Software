"""
Faster Whisper Large-v3 transcriber untuk ICAN CLIP.
Word-level timestamps untuk subtitle kata-per-kata.
"""
import os

import torch
from faster_whisper import WhisperModel

from config_ican import WHISPER_MODEL


class IcanWhisperTranscriber:
    """Transkripsi audio dengan Faster Whisper large-v3."""

    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        if self._model is not None:
            return
        print(f"🎵 Loading Faster Whisper ({WHISPER_MODEL})...")
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            compute_type = "float16" if device == "cuda" else "int8"
            os.environ["OMP_NUM_THREADS"] = "2"
            self._model = WhisperModel(
                WHISPER_MODEL,
                device=device,
                compute_type=compute_type,
                cpu_threads=4,
                num_workers=2,
            )
            print(f"✅ Whisper loaded: {device} / {compute_type}")
        except Exception as e:
            print(f"⚠️  Fallback CPU: {e}")
            self._model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")

    def transcribe(self, video_path, language=None):
        """
        Transkripsi video dengan word timestamps.

        Returns:
            tuple: (words, full_text, segments, detected_language)
        """
        print("🎵 Transcribing dengan Faster Whisper large-v3...")
        kwargs = {
            'word_timestamps': True,
            'vad_filter': True,
            'vad_parameters': {'min_silence_duration_ms': 400},
            'beam_size': 5,
            'best_of': 1,
        }
        if language:
            kwargs['language'] = language

        segments_iter, info = self._model.transcribe(str(video_path), **kwargs)
        detected_lang = info.language if info else 'unknown'

        words = []
        segments_list = []
        full_text = ""

        for segment in segments_iter:
            segments_list.append({
                'id': segment.id,
                'start': segment.start,
                'end': segment.end,
                'text': segment.text.strip(),
            })
            full_text += segment.text + " "

            if segment.words:
                for w in segment.words:
                    word = w.word.strip().upper()
                    if word:
                        words.append({
                            'word': word,
                            'start': w.start,
                            'end': w.end,
                        })

        print(
            f"✅ Transkripsi selesai: {len(words)} kata, "
            f"{len(segments_list)} segmen, bahasa={detected_lang}"
        )
        return words, full_text.strip(), segments_list, detected_lang
