"""
Configuration settings for the Voice Cloning Engine.

This module centralizes all configuration constants, paths, and settings
used throughout the application.
"""
import os
from pathlib import Path

# ============================================================================
# Project Paths
# ============================================================================
PROJECT_ROOT = Path(__file__).parent.absolute()
MODELS_DIR = PROJECT_ROOT / "Models"
SAMPLES_DIR = PROJECT_ROOT / "samples"
TEMP_OUTPUT_PATH = PROJECT_ROOT / "temp_output.wav"

# Ensure directories exist
SAMPLES_DIR.mkdir(exist_ok=True)

# ============================================================================
# Model Configuration
# ============================================================================
MODEL_BACKBONE_LOCAL = MODELS_DIR / "neutts-air"
MODEL_BACKBONE_REPO = "neutts-air-q4-gguf"
MODEL_CODEC_REPO = "neuphonic/neucodec"
MODEL_DEVICE = "cpu"

# ============================================================================
# Audio Parameters
# ============================================================================
SAMPLE_RATE = 24000
SILENCE_DURATION = 0.25  # seconds between chunks
SPEED_MIN = 0.5
SPEED_MAX = 2.0
SPEED_DEFAULT = 1.0
SPEED_STEP = 0.1

# ============================================================================
# Text Processing
# ============================================================================
MAX_CHUNK_LENGTH = 150  # characters per chunk

# ============================================================================
# UI Configuration
# ============================================================================
SERVER_NAME = "localhost"
SERVER_PORT = 7860
SHARE_GRADIO = False
OPEN_BROWSER = True
SHOW_ERROR = True

# ============================================================================
# eSpeak Paths (Windows)
# ============================================================================
ESPEAK_POSSIBLE_PATHS = [
    "C:\\Program Files\\eSpeak NG",
    "C:\\Program Files (x86)\\eSpeak NG",
    "C:\\Program Files\\eSpeak",
    "C:\\Program Files (x86)\\eSpeak",
]

ESPEAK_DLL_NAMES = [
    'libespeak-ng.dll',
    'espeak-ng.dll',
    'libespeak.dll',
    'espeak.dll'
]

ESPEAK_COMMANDS = ['espeak-ng', 'espeak']
