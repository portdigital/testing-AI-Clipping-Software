"""
ICAN CLIP — Pipeline utama mirip Opus Clip.

YouTube URL → yt-dlp → Faster Whisper large-v3 → Pyannote Diarization
→ Gemini 2.5 Flash → Hook Detection → Virality Scoring
→ YOLO Face Tracking → Word Subtitle → Auto Reframe 9:16 → Export Shorts
"""
import re
from pathlib import Path

from moviepy.editor import VideoFileClip

from config_ican import OUTPUT_DIR, TEMP_DIR
from services.youtube_downloader_yt_dlp import YouTubeDownloader
from services.ican_whisper import IcanWhisperTranscriber
from services.speaker_diarizer import SpeakerDiarizer
from services.ican_gemini_analyzer import IcanGeminiAnalyzer
from services.hook_detector import HookDetector
from services.virality_scorer import ViralityScorer
from services.yolo_face_tracker import YOLOFaceTracker
from services.caption_maker import CaptionMaker
from utils.helpers import generate_random_clips, cleanup_temp_files


class IcanProcessor:
    """Orkestrator pipeline ICAN CLIP."""

    def __init__(self, caption_style='clean_white', use_subtitles=True):
        self.downloader = YouTubeDownloader(temp_dir=TEMP_DIR)
        self.transcriber = IcanWhisperTranscriber()
        self.diarizer = SpeakerDiarizer()
        self.gemini = IcanGeminiAnalyzer()
        self.hook_detector = HookDetector()
        self.virality_scorer = ViralityScorer()
        self.face_tracker = YOLOFaceTracker()
        self.caption_maker = CaptionMaker(caption_style)
        self.use_subtitles = use_subtitles
        self.caption_style = caption_style

    def process(self, url, num_clips, min_duration, max_duration, language=None):
        """
        Jalankan full pipeline ICAN CLIP.

        Returns:
            tuple: (output_files, video_title, clip_metadata)
        """
        print("\n" + "=" * 60)
        print("🚀 ICAN CLIP — Starting Pipeline")
        print("=" * 60)

        # Step 1: yt-dlp download
        print("\n📥 [1/10] Downloading via yt-dlp...")
        video_path, title, duration = self.downloader.download(url)
        print(f"✅ Downloaded: {title} ({duration:.1f}s)")

        # Step 2: Faster Whisper large-v3
        print("\n🎵 [2/10] Transcribing with Faster Whisper large-v3...")
        words, transcript, segments, detected_lang = self.transcriber.transcribe(
            video_path, language=language
        )

        # Step 3: Pyannote diarization
        print("\n🎙️  [3/10] Speaker diarization (Pyannote)...")
        speaker_turns = self.diarizer.diarize(video_path)
        segments = self.diarizer.assign_speakers_to_segments(segments, speaker_turns)

        # Step 4: Gemini 2.5 Flash clip selection
        print("\n🧠 [4/10] AI clip selection (Gemini 2.5 Flash)...")
        if not segments:
            print("⚠️  Transkripsi kosong — random clips")
            clip_specs = generate_random_clips(duration, num_clips, min_duration, max_duration)
        else:
            clip_specs = self.gemini.select_clips(
                segments, duration, num_clips, min_duration, max_duration
            )

        if not clip_specs:
            raise ValueError("Tidak ada klip yang bisa dipilih.")

        # Step 5: Hook detection
        print("\n🪝 [5/10] Hook detection...")
        clip_specs = self.hook_detector.enrich_clips(clip_specs, segments)

        # Step 6: Virality scoring
        print("\n⭐ [6/10] Virality scoring...")
        clip_specs = self.virality_scorer.rank_clips(clip_specs, segments, top_n=num_clips)

        # Steps 7-10: per-clip processing
        output_files = []
        metadata = []

        print(f"\n🎬 [7-10/10] Processing {len(clip_specs)} clips...")
        for i, clip_info in enumerate(clip_specs, 1):
            output = self._process_single_clip(
                video_path, clip_info, words, i, len(clip_specs)
            )
            if output:
                output_files.append(output['path'])
                metadata.append(output)

        self.face_tracker.close()
        cleanup_temp_files()

        print("\n" + "=" * 60)
        print(f"🎉 ICAN CLIP selesai — {len(output_files)} Shorts diekspor")
        print("=" * 60)

        return output_files, title, metadata

    def _process_single_clip(self, video_path, clip_info, words, index, total):
        start = clip_info['start']
        end = clip_info['end']
        title_text = clip_info.get('title', f'Clip {index}')
        score = clip_info.get('virality_score', 0)
        hook_type = clip_info.get('hook_type', 'general')

        print(f"\n📹 Clip {index}/{total}: {title_text}")
        print(f"   ⭐ Virality: {score}/100 | 🪝 Hook: {hook_type}")
        print(f"   ⏱️  {start:.1f}s → {end:.1f}s")

        try:
            with VideoFileClip(str(video_path)) as video:
                clip = video.subclip(start, end)

                # Step 7: YOLO face tracking + Step 9: auto reframe 9:16
                print("   🎯 YOLO tracking + reframe 9:16...")
                clip = self.face_tracker.track_and_reframe(clip)

                # Step 8: word-by-word subtitles
                if self.use_subtitles and words:
                    print("   📝 Adding word subtitles...")
                    clip = self.caption_maker.add_captions(clip, words, start)

                # Step 10: export Shorts
                safe_title = re.sub(r'[^\w\s-]', '', title_text)[:40].strip().replace(' ', '_')
                filename = f"ican_{index}_{int(score)}pts_{safe_title}.mp4"
                output_path = OUTPUT_DIR / filename

                print(f"   🎥 Exporting Shorts → {filename}")
                clip.write_videofile(
                    str(output_path),
                    codec='libx264',
                    audio_codec='aac',
                    preset='medium',
                    fps=30,
                    ffmpeg_params=['-crf', '18', '-pix_fmt', 'yuv420p'],
                    verbose=False,
                    logger=None,
                    temp_audiofile=str(TEMP_DIR / f'audio_{index}.m4a'),
                    remove_temp=True,
                    threads=4,
                )

                print(f"   ✅ Exported: {filename}")
                return {
                    'path': str(output_path),
                    'title': title_text,
                    'virality_score': score,
                    'hook_type': hook_type,
                    'hook_score': clip_info.get('hook_score', 0),
                    'start': start,
                    'end': end,
                }

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
