"""
Virality Scoring — skor komposit mirip Opus Clip.
Menggabungkan AI score, hook score, durasi, dan engagement signals.
"""
OPTIMAL_DURATION_RANGE = (25, 45)


class ViralityScorer:
    """Hitung skor virality final untuk ranking klip."""

    WEIGHTS = {
        'ai_score': 0.40,
        'hook_score': 0.30,
        'duration_score': 0.15,
        'engagement_score': 0.15,
    }

    def _duration_score(self, duration):
        """Skor berdasarkan durasi ideal Shorts (25-45 detik)."""
        low, high = OPTIMAL_DURATION_RANGE
        if low <= duration <= high:
            return 100
        if duration < low:
            return max(50, 100 - (low - duration) * 5)
        return max(40, 100 - (duration - high) * 3)

    def _engagement_score(self, segments, clip_start, clip_end):
        """Skor berdasarkan kepadatan bicara dan pergantian speaker."""
        clip_segments = [
            s for s in segments
            if s['start'] < clip_end and s['end'] > clip_start
        ]
        if not clip_segments:
            return 50

        duration = clip_end - clip_start
        words = sum(len(s['text'].split()) for s in clip_segments)
        wpm = (words / duration) * 60 if duration > 0 else 0

        speakers = {s.get('speaker', 'SPEAKER_00') for s in clip_segments}
        speaker_bonus = 10 if len(speakers) > 1 else 0

        if 120 <= wpm <= 180:
            pace_score = 90
        elif 80 <= wpm < 120 or 180 < wpm <= 220:
            pace_score = 70
        else:
            pace_score = 55

        return min(100, pace_score + speaker_bonus)

    def score_clip(self, clip, segments):
        """Hitung virality score komposit untuk satu klip."""
        ai_score = clip.get('virality_score', clip.get('ai_score', 50))
        hook_score = clip.get('hook_score', 50)
        duration = clip.get('duration', clip['end'] - clip['start'])

        dur_score = self._duration_score(duration)
        eng_score = self._engagement_score(segments, clip['start'], clip['end'])

        composite = (
            ai_score * self.WEIGHTS['ai_score']
            + hook_score * self.WEIGHTS['hook_score']
            + dur_score * self.WEIGHTS['duration_score']
            + eng_score * self.WEIGHTS['engagement_score']
        )

        return {
            **clip,
            'ai_score': ai_score,
            'duration_score': round(dur_score, 1),
            'engagement_score': round(eng_score, 1),
            'virality_score': round(composite, 1),
        }

    def rank_clips(self, clips, segments, top_n=None):
        """Skor dan urutkan klip berdasarkan virality."""
        scored = [self.score_clip(c, segments) for c in clips]
        scored.sort(key=lambda x: x['virality_score'], reverse=True)

        print(f"⭐ Virality scoring selesai — top klip:")
        for i, c in enumerate(scored[:top_n or len(scored)], 1):
            print(
                f"   {i}. {c.get('title', 'Untitled')} — "
                f"⭐{c['virality_score']}/100 "
                f"(AI:{c['ai_score']} Hook:{c['hook_score']} "
                f"Dur:{c['duration_score']} Eng:{c['engagement_score']})"
            )

        return scored[:top_n] if top_n else scored
