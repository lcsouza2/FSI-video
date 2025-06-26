from core.download import Video
from fastapi import FastAPI, Request, Query, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import shutil
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from core.transcribe import assign_speakers_to_segments, transcribe_audio, recognize_speakers

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


@MAIN_APP.post("/process/fromfile")
async def process_from_file(
    file: UploadFile = File(...)
    ):

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name


    #Commented to use default data for testing
    # transcript = transcribe_audio(tmp_path)
    # diarization = recognize_speakers(tmp_path)

    #Default data:
    with open("./pyannote.json", "r") as file:
        transcript = json.load(file)

    with open("./whisper.json", "r") as file:
        diarization = json.load(file)

    assign_speakers_to_segments(transcript, diarization)

    return (transcript, diarization)