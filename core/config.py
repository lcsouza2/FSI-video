from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    #Audio configration for downloading and processing
    AUDIO_FORMAT: str ="bestaudio/best"
    AUDIO_DOWNLOAD_PATH: str = f"static/audio.%(ext)s"
    POST_PROCESSORS = [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }]

    FFMPEG_PATH: str = "/usr/bin/ffmpeg" # Adjust this path to your ffmpeg installation
    CHUNK_LENGHT_MS = 60 * 1000

    #AssemblyAI model configuration
    BASE_URL = "https://api.assemblyai.com"
    AUTH_TOKEN = "b1d3b6047bc54d01a16802521c5f5c6c"
    SPEECH_MODEL = "universal"
    DEFAULT_HEADERS: dict = {
        "authorization": AUTH_TOKEN
    }

    TRANSCRIPTION_FORMAT: str = "txt"
    TRANSCRITPION_PATH: str = "static/transcript.txt"
