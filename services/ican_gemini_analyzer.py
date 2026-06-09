"""
Gemini 2.5 Flash — analisis transkrip dengan konteks speaker diarization.
Memilih klip viral terbaik mirip Opus Clip.
"""
import json
import random

import google.generativeai as genai

from config_ican import GEMINI_API_KEY, GEMINI_MODEL


class IcanGeminiAnalyzer:
    """AI clip selection dengan Gemini 2.5 Flash."""

    def __init__(self, api_key=None):
        self.api_key = api_key or GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = self._init_model()

    def _init_model(self):
        candidates = [GEMINI_MODEL, 'gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-1.5-pro']
        for name in candidates:
            try:
                model = genai.GenerativeModel(name)
                print(f"✅ Gemini model: {name}")
                return model
            except Exception as e:
                print(f"⚠️  Model {name} tidak tersedia: {e}")
        raise ValueError("Tidak ada model Gemini yang kompatibel.")

    def _format_transcript(self, segments):
        lines = []
        for seg in segments:
            speaker = seg.get('speaker', 'SPEAKER')
            lines.append(
                f"[{seg['start']:.1f}s-{seg['end']:.1f}s] {speaker}: {seg['text']}"
            )
        return '\n'.join(lines)

    def select_clips(self, segments, video_duration, n, min_dur, max_dur):
        """Pilih klip viral terbaik dari transkrip ber-label speaker."""
        transcript = self._format_transcript(segments)
        speakers = {s.get('speaker') for s in segments}
        has_diarization = len(speakers) > 1

        prompt = f"""You are an expert viral short-form content editor like Opus Clip.
Analyze this transcript and select the {n} BEST clips for YouTube Shorts / TikTok / Reels.

{"Speaker diarization is available — prefer clips with clear single-speaker moments or dynamic multi-speaker exchanges." if has_diarization else ""}

CRITICAL RULES:
1. Each clip MUST be a COMPLETE thought — never cut mid-sentence
2. Duration: {min_dur}-{max_dur} seconds (use EXACT timestamps from transcript)
3. Clips must NOT overlap
4. Prioritize: strong hooks, revelations, emotional peaks, actionable advice, funny moments, hot takes
5. First 3 seconds must grab attention (hook-worthy opening)

VIDEO DURATION: {video_duration:.1f} seconds

TRANSCRIPT:
{transcript}

Return ONLY valid JSON:
{{
  "clips": [
    {{
      "start": 12.5,
      "end": 45.0,
      "title": "Catchy clip title",
      "virality_score": 88,
      "hook_type": "question|shocking|story|controversy|promise|general",
      "reason": "Why this clip will go viral"
    }}
  ]
}}"""

        try:
            print("🧠 Gemini 2.5 Flash menganalisis transkrip...")
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"},
            )
            data = json.loads(response.text)
            return self._validate_clips(data.get('clips', []), video_duration, min_dur, max_dur, n)
        except Exception as e:
            print(f"❌ Gemini gagal: {e} — menggunakan fallback")
            return self._fallback(segments, video_duration, n, min_dur, max_dur)

    def _validate_clips(self, raw_clips, video_duration, min_dur, max_dur, n):
        validated = []
        for clip in raw_clips:
            start = clip.get('start')
            end = clip.get('end')
            if start is None or end is None:
                continue

            start, end = float(start), float(end)
            duration = end - start
            if duration > max_dur:
                end = start + max_dur
                duration = max_dur

            if min_dur <= duration <= max_dur and 0 <= start < end <= video_duration:
                validated.append({
                    'start': start,
                    'end': end,
                    'title': clip.get('title', 'Untitled'),
                    'virality_score': clip.get('virality_score', 70),
                    'hook_type': clip.get('hook_type', 'general'),
                    'reason': clip.get('reason', ''),
                    'duration': duration,
                })

        validated.sort(key=lambda x: x['virality_score'], reverse=True)
        print(f"✅ Gemini memilih {len(validated[:n])} klip kandidat")
        return validated[:n]

    def _fallback(self, segments, video_duration, n, min_dur, max_dur):
        clips = []
        used = set()
        for i in range(n):
            available = [s for j, s in enumerate(segments) if j not in used]
            if not available:
                break
            seg = random.choice(available)
            idx = segments.index(seg)
            used.add(idx)
            start = seg['start']
            end = min(start + max_dur, seg['end'] + 10, video_duration)
            if end - start < min_dur:
                end = min(start + min_dur, video_duration)
            clips.append({
                'start': start,
                'end': end,
                'title': f'Clip {i + 1}',
                'virality_score': 50,
                'hook_type': 'general',
                'duration': end - start,
            })
        return clips
