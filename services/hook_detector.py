"""
Hook Detection — analisis 3-5 detik pembuka setiap klip kandidat.
Mirip Opus Clip: deteksi pola hook yang menarik perhatian.
"""
import re

HOOK_PATTERNS = {
    'question': re.compile(
        r'\?|^(apa|bagaimana|kenapa|mengapa|siapa|kapan|dimana|what|how|why|who|when|where)\b',
        re.IGNORECASE,
    ),
    'shocking': re.compile(
        r'\b(rahasia|secret|shocking|gila|unbelievable|never|tidak pernah|jangan|don\'t|stop)\b',
        re.IGNORECASE,
    ),
    'number': re.compile(r'\b\d+[%+]?\b'),
    'story': re.compile(
        r'\b(cerita|story|dulu|waktu itu|one day|tiba-tiba|suddenly|kemarin|yesterday)\b',
        re.IGNORECASE,
    ),
    'controversy': re.compile(
        r'\b(salah|wrong|kebohongan|lie|hot take|kontroversial|debate|versus|vs)\b',
        re.IGNORECASE,
    ),
    'promise': re.compile(
        r'\b(gratis|free|mudah|easy|cepat|fast|tips|hack|trick|cara|how to)\b',
        re.IGNORECASE,
    ),
}

HOOK_TYPE_WEIGHTS = {
    'question': 85,
    'shocking': 90,
    'number': 75,
    'story': 80,
    'controversy': 88,
    'promise': 78,
    'general': 50,
}


class HookDetector:
    """Deteksi kekuatan hook pada pembuka klip."""

    def __init__(self, hook_window_seconds=5.0):
        self.hook_window = hook_window_seconds

    def _get_opening_text(self, segments, clip_start, clip_end):
        """Ambil teks 3-5 detik pertama klip."""
        opening_end = clip_start + self.hook_window
        texts = []
        for seg in segments:
            if seg['end'] <= clip_start:
                continue
            if seg['start'] >= opening_end:
                break
            texts.append(seg['text'].strip())
        return ' '.join(texts)

    def detect(self, segments, clip_start, clip_end, existing_hook_type=None):
        """
        Analisis hook pada pembuka klip.

        Returns:
            dict: hook_type, hook_score (0-100), hook_text, hook_reason
        """
        opening_text = self._get_opening_text(segments, clip_start, clip_end)

        if not opening_text:
            return {
                'hook_type': existing_hook_type or 'general',
                'hook_score': 40,
                'hook_text': '',
                'hook_reason': 'Tidak ada teks pembuka terdeteksi',
            }

        detected_types = []
        for hook_type, pattern in HOOK_PATTERNS.items():
            if pattern.search(opening_text):
                detected_types.append(hook_type)

        if detected_types:
            primary_type = max(detected_types, key=lambda t: HOOK_TYPE_WEIGHTS[t])
            base_score = HOOK_TYPE_WEIGHTS[primary_type]
            bonus = min(10, (len(detected_types) - 1) * 5)
            hook_score = min(100, base_score + bonus)
            reason = f"Hook {primary_type}: '{opening_text[:60]}...'"
        else:
            primary_type = existing_hook_type or 'general'
            word_count = len(opening_text.split())
            hook_score = 55 if word_count >= 5 else 45
            reason = f"Pembuka standar ({word_count} kata)"

        return {
            'hook_type': primary_type,
            'hook_score': hook_score,
            'hook_text': opening_text[:120],
            'hook_reason': reason,
        }

    def enrich_clips(self, clips, segments):
        """Tambahkan hook analysis ke setiap klip kandidat."""
        enriched = []
        for clip in clips:
            hook = self.detect(
                segments,
                clip['start'],
                clip['end'],
                clip.get('hook_type'),
            )
            clip.update(hook)
            enriched.append(clip)

        print(f"🪝 Hook detection selesai untuk {len(enriched)} klip")
        for i, c in enumerate(enriched, 1):
            print(f"   {i}. [{c['hook_type']}] score={c['hook_score']} — {c['hook_text'][:50]}...")

        return enriched
