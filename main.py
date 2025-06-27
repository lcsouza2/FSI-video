from core.download import Video
from fastapi import FastAPI, Request, Query, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import re
import tempfile
import shutil
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from core.transcribe import assign_speakers_to_segments
from core.data_analysis import get_interest_points, get_total_time, remove_stop_words
from core.wordcloud_gen import generate_from_str
from datetime import timedelta

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
    file: UploadFile = File(...),
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
        diarization = json.load(file)

    with open("./whisper.json", "r") as file:
        transcript = json.load(file)

    final_brute = assign_speakers_to_segments(transcript, diarization)

    final_string = "".join(
        ["{}: {}\n".format(segment["speaker"], segment["text"]) for segment in final_brute]
    )

    without_stop_words = remove_stop_words(transcript["text"])

    candidates = []

    for speaker in list(set(seg["speaker"] for seg in final_brute)):
        total_time = timedelta()
        word_count = 0
        full_text = []

        for segment in final_brute:
            if segment["speaker"] == speaker:
                total_time += get_total_time([segment])
                word_count += len(segment["text"].split())
                full_text.append(segment["text"])

        candidates.append({
            "name": speaker,
            "total_time": total_time,
            "word_count": word_count,
            "full_text": full_text,
            "most_used_word": max(
                set(" ".join(full_text).split()), key=" ".join(full_text).split().count
            ),
            "wordcloud": generate_from_str(" ".join(full_text)),
        })

    return {
        "brute_result": final_brute,
        "result": final_string,
        "total_words": len(transcript["text"].split()),
        "duration": get_total_time(final_brute),
        "most_used_word": max(
            set(without_stop_words.split()), key=without_stop_words.split().count
        ),
        "wordcloud": generate_from_str(without_stop_words),
        "interest_points": re.findall(r"@point:\s*(.*?)\s*;", get_interest_points(final_string)),
        "candidates": candidates
        }


@MAIN_APP.get("/wordcloud")
async def return_wordcloud(filename: str = Query()):
    if not filename:
        raise HTTPException(400, "Caminho não pode ser vazio")

    if not os.path.exists(filename):
        raise HTTPException(500, "Erro ao encontrar nuvem de palavras")

    return FileResponse(path=filename, filename="wordcloud.png")