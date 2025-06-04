from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    AUDIO_FORMAT: str ="bestaudio/best"
    TARGET_DOWNLOAD_PATH: str = f"static/audio.%(ext)s"
    POST_PROCESSORS: List[dict] = [
        {
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }
    ],
    FFMPEG_PATH: str = "./ffmpeg/bin"
    CHUNK_LENGHT_MS = 60 * 1000 
    