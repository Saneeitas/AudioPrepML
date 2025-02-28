# AudioPrepML

AudioPrepML is a Python-based toolkit for preparing audio datasets for machine learning, specifically designed for finetuning text-to-speech (TTS) models. It includes scripts to convert MP3 files to WAV format and split audio into labeled chunks with corresponding transcript files, optimized for multi-speaker training.

## Features
- **MP3 to WAV Conversion**: Converts MP3 audio files to 24 kHz, 16-bit, mono WAV format, suitable for XTTS-v2.
- **Audio Splitting**: Splits audio into 15-second (or less) chunks based on silence detection, with speaker-specific naming (e.g., `jane_1.wav`) and matching empty transcript files (e.g., `jane_1.txt`).
- **XTTS Compatibility**: Outputs audio at 24 kHz, 16-bit, mono, aligning with XTTS-v2’s native requirements.

## Prerequisites
- **Python**: 3.7 or higher
- **Dependencies**:
  - `pydub`: For audio processing (`pip install pydub`)
- **FFmpeg**: Required by `pydub` for audio format conversion and resampling. Install it:
  - **Ubuntu/Linux**: `sudo apt-get install ffmpeg`
  - **MacOS**: `brew install ffmpeg`
  - **Windows**: Download from [FFmpeg site](https://ffmpeg.org/download.html) and add to PATH.

## Installation
1. Clone this repo: `git clone https://github.com/yourusername/AudioPrepML.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Install `ffmpeg` (required by pydub):
   - Windows: `choco install ffmpeg` (via Chocolatey)
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg`
