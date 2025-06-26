from core.audio_operations import Video
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

MAIN_APP = FastAPI()
MAIN_APP.mount("/statics", StaticFiles(directory="./templates/statics"), "static")

templates_folder = Jinja2Templates("./templates/")
MAIN_APP.add_middleware(CORSMiddleware, allow_origins=["*"])


@MAIN_APP.get("/")
async def lading_page(request: Request):
    return templates_folder.TemplateResponse(request=request, name="index.html")


@MAIN_APP.post("/download/audio")
async def return_downloaded_audio(url: str = Query()):
    """
    Downloads the audio from the given video URL using yt-dlp.

    Returns:
        FileResponse: Response with downloaded audio file.
    """

    file = Video(url).download_audio()

    if not os.path.exists(file):
        raise HTTPException(500, "Erro buscando arquivo baixado")

    return FileResponse(path=file, filename="Audio_baixado.mp3")


@MAIN_APP.post("/download/video")
async def return_downloaded_video(url: str = Query()):
    """
    Downloads the video from the given video URL using yt-dlp.

    Returns:
        FileResponse: Response with downloaded audio file.
    """
    file = Video(url, "video").download_video()

    if not os.path.exists(file):
        raise HTTPException(500, "Erro buscando arquivo baixado")

    return FileResponse(path=file, filename="Audio_baixado")
