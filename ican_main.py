#!/usr/bin/env python3
"""
ICAN CLIP — Auto Short-Form Generator (Opus Clip style)

Pipeline:
  YouTube URL → yt-dlp → Faster Whisper large-v3 → Pyannote Diarization
  → Gemini 2.5 Flash → Hook Detection → Virality Scoring
  → YOLO Face Tracking → Word Subtitle → Auto Reframe 9:16 → Export Shorts
"""
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from config_ican import (
    OUTPUT_DIR, TEMP_DIR,
    DEFAULT_NUM_CLIPS, DEFAULT_MIN_DURATION, DEFAULT_MAX_DURATION,
)
from services.ican_processor import IcanProcessor
from styles.caption_styles import CAPTION_STYLES


def log(msg):
    print(msg, flush=True)


def validate_youtube_url(url):
    if not url:
        return False
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc and
                ('youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc))


def display_styles():
    log("\n🎨 Gaya Subtitle:")
    log("=" * 40)
    keys = list(CAPTION_STYLES.keys())
    for i, (key, val) in enumerate(CAPTION_STYLES.items(), 1):
        log(f"  {i}. {key} — {val['name']}")
    log("=" * 40)
    return keys


def main(url=None):
    log("╔══════════════════════════════════════════╗")
    log("║         🎬 ICAN CLIP v1.0               ║")
    log("║   Auto Short-Form Generator (Opus Style) ║")
    log("╚══════════════════════════════════════════╝")
    log("")
    log("Pipeline: yt-dlp → Whisper large-v3 → Pyannote → Gemini 2.5 Flash")
    log("          → Hook Detection → Virality Score → YOLO → Subtitle → 9:16")
    log("")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    if not url:
        url = input("🔗 YouTube URL: ").strip()
    if not validate_youtube_url(url):
        log("❌ URL YouTube tidak valid.")
        return

    try:
        num_clips = int(input(f"📊 Jumlah klip [{DEFAULT_NUM_CLIPS}]: ") or str(DEFAULT_NUM_CLIPS))
        max_dur = int(input(f"⏱️  Max detik/klip [{DEFAULT_MAX_DURATION}]: ") or str(DEFAULT_MAX_DURATION))
        min_dur = int(input(f"⏱️  Min detik/klip [{DEFAULT_MIN_DURATION}]: ") or str(DEFAULT_MIN_DURATION))

        if min_dur >= max_dur:
            log("❌ Min duration harus lebih kecil dari max duration.")
            return

        style_keys = display_styles()
        choice = input(f"🎨 Pilih gaya subtitle (1-{len(style_keys)}) [1]: ").strip() or "1"
        try:
            style = style_keys[int(choice) - 1]
        except (ValueError, IndexError):
            style = 'clean_white'

        sub_choice = input("📝 Aktifkan word subtitle? [Y/n]: ").strip().lower()
        use_subs = sub_choice != 'n'

        lang = input("🌐 Bahasa (kosongkan = auto-detect): ").strip() or None

        log("\n" + "=" * 60)
        log("🚀 Memulai ICAN CLIP...")
        log("=" * 60)

        processor = IcanProcessor(caption_style=style, use_subtitles=use_subs)
        time.sleep(0.3)

        outputs, title, metadata = processor.process(
            url, num_clips, min_dur, max_dur, language=lang
        )

        log("\n" + "=" * 60)
        log("🎉 SHORTS SIAP!")
        log("=" * 60)
        log(f"📹 Sumber: {title}")
        log(f"📁 Folder: {OUTPUT_DIR.resolve()}")
        log(f"🎨 Subtitle: {CAPTION_STYLES[style]['name']}")
        log("")

        total_mb = 0
        for i, (path, meta) in enumerate(zip(outputs, metadata), 1):
            p = Path(path)
            if p.exists():
                mb = p.stat().st_size / (1024 * 1024)
                total_mb += mb
                log(f"  {i}. {p.name}")
                log(f"     ⭐ {meta['virality_score']}/100 | 🪝 {meta['hook_type']} | {mb:.1f} MB")

        log(f"\n💾 Total: {total_mb:.1f} MB | {len(outputs)} klip")
        log("✅ Selesai!")

    except KeyboardInterrupt:
        log("\n🛑 Dibatalkan.")
    except Exception as e:
        log(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    cli_url = sys.argv[1].strip() if len(sys.argv) > 1 else None
    if cli_url and not cli_url.startswith('http'):
        cli_url = 'https://' + cli_url
    main(cli_url)
