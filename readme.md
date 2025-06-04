# YouTube Video Analysis Tool

A Python tool that downloads audio from YouTube videos, transcribes the content, analyzes it using LLM to extract key points, and generates a word cloud visualization.

## Features

- YouTube audio extraction
- Speech-to-text transcription using Whisper
- Key points extraction using LLM analysis
- Word cloud generation
- Support for long videos through chunk processing

## Prerequisites

- Python 3.11 or higher
- FFmpeg installed on your system
- Poetry for dependency management

## Installation

1. First, install FFmpeg:

   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

   **macOS:**
   ```bash
   brew install ffmpeg
   ```

   **Windows:**
   Download from [FFmpeg official website](https://ffmpeg.org/download.html)

2. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [project-directory]
   ```

3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Usage

1. Activate the poetry environment:
   ```bash
   poetry shell
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

## Project Structure

```
.
├── audio_getter.py    # YouTube audio download functionality
├── config.py          # Configuration settings
├── main.py           # Main application script
├── static/           # Directory for downloaded audio files
├── poetry.lock       # Poetry lock file
└── pyproject.toml    # Project dependencies
```

## Dependencies

- pyaudio
- openai-whisper
- yt-dlp
- ffprobe
- ffmpeg-python
- pydub
