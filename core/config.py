from dataclasses import dataclass


@dataclass
class Config:
    # Audio configration for downloading and processing
    AUDIO_FORMAT: str = "bestaudio/best"
    VIDEO_FORMAT: str = "bestvideo+bestaudio/best"
    POST_PROCESSORS = [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ]

    FFMPEG_PATH: str = "/usr/bin/ffmpeg"  # Adjust this path to your ffmpeg installation

    GENAI_API_KEY: str = "AIzaSyB0fB_f5ktPvsTe7znzqxrIgQHEkcHtb1o"
