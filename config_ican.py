"""
Configuration for ICAN CLIP — Opus Clip-style auto short-form generator.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_API_KEY_HERE')
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')

# Directories
OUTPUT_DIR = Path(os.getenv('ICAN_OUTPUT_DIR', './ican_clips'))
TEMP_DIR = Path(os.getenv('ICAN_TEMP_DIR', './ican_temp'))

# Models
WHISPER_MODEL = os.getenv('ICAN_WHISPER_MODEL', 'large-v3')
GEMINI_MODEL = os.getenv('ICAN_GEMINI_MODEL', 'gemini-2.5-flash')
YOLO_MODEL = os.getenv('ICAN_YOLO_MODEL', 'yolov8n.pt')

# YouTube download (yt-dlp)
YOUTUBE_USER_AGENT = os.getenv(
    'YOUTUBE_USER_AGENT',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
)
YOUTUBE_COOKIES_CONTENT = os.getenv('YOUTUBE_COOKIES_CONTENT', '')

# Clip defaults
DEFAULT_NUM_CLIPS = int(os.getenv('ICAN_NUM_CLIPS', '5'))
DEFAULT_MIN_DURATION = int(os.getenv('ICAN_MIN_DURATION', '15'))
DEFAULT_MAX_DURATION = int(os.getenv('ICAN_MAX_DURATION', '60'))

# Export settings (YouTube Shorts / TikTok / Reels)
EXPORT_WIDTH = 1080
EXPORT_HEIGHT = 1920
EXPORT_FPS = 30

OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

if "YOUR_API_KEY_HERE" in GEMINI_API_KEY:
    print("⚠️  ICAN CLIP: Set GEMINI_API_KEY di file .env")

if not HUGGINGFACE_TOKEN:
    print("⚠️  ICAN CLIP: Set HUGGINGFACE_TOKEN untuk Pyannote diarization (opsional)")
