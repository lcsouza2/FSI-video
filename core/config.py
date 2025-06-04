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

    #Whisper model configuration
    WHISPER_MODEL: str = "base"
    TRANSCRIPTION_FORMAT: str = "txt"
    TRANSCRITPION_PATH: str = "static/transcript.txt"
