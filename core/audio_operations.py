from yt_dlp import YoutubeDL
from core.config import Config
from http.client import BAD_REQUEST
from fastapi import HTTPException
import os
import uuid

DOWNLOAD_DIR = "./downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


class Video:
    def __init__(self, url: str, mode: str = "audio"):
        if not url:
            raise HTTPException(BAD_REQUEST, "Url do vídeo não recebida")

        self.url = url.strip()
        self.id = str(uuid.uuid4())
        self.mode = mode

    def get_ydl_opts(self):
        if self.mode not in ("audio", "video"):
            raise HTTPException(400, "Formato inválido, tente um áudio ou vídeo")

        if self.mode == "audio":
            return {
                "format": Config.AUDIO_FORMAT,
                "outtmpl": os.path.join(DOWNLOAD_DIR, f"audio/{self.id}.%(ext)s"),
                "postprocessors": Config.POST_PROCESSORS,
                "ffmpeg_location": Config.FFMPEG_PATH,
            }

        return {
            "format": Config.VIDEO_FORMAT,
            "outtmpl": os.path.join(DOWNLOAD_DIR, f"video/{self.id}.%(ext)s"),
        }

    def download_audio(self) -> str:
        with YoutubeDL(self.get_ydl_opts()) as ydl:
            info = ydl.extract_info(self.url, download=True)
            return self.process_filename(ydl.prepare_filename(info))

    def download_video(self) -> str:
        with YoutubeDL(self.get_ydl_opts()) as ydl:
            info = ydl.extract_info(self.url, download=True)
            return ydl.prepare_filename(info)

    def process_filename(self, filename: str) -> str:
        return (
            filename.replace(".webm", ".mp3")
            .replace(".m4a", ".mp3")
            .replace(".opus", ".mp3")
        )
