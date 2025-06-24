from yt_dlp import YoutubeDL
from core.config import Config
import requests
import time

ydl_opts = {
    'format': Config.AUDIO_FORMAT,
    'outtmpl': Config.AUDIO_DOWNLOAD_PATH,
    'postprocessors': Config.POST_PROCESSORS,
    'ffmpeg_location': Config.FFMPEG_PATH,
}

def download_audio(video_url: str, output_path:str | None = None) -> str:
    """
    Downloads the audio from the given video URL using yt-dlp.

    Returns:
        str: The path to the downloaded audio file.
    """

    if output_path:
        ydl_opts['outtmpl'] = output_path

    if not video_url:
        print("No video URL provided.")
        return ""

    print("Formatando URL do vídeo...\n")
    video_url = video_url.strip()
    print("Sucesso\n")

    with YoutubeDL(ydl_opts) as ydl:
        try:
            print("Baixando vídeo...\n")
            ydl.download([video_url])
            return ydl.prepare_filename(ydl.extract_info(video_url, download=False))
        except Exception as e:
            print(f"Error downloading: {e}")
            return ""

def upload_audio_file_to_model(
    audio_path: str = Config.AUDIO_DOWNLOAD_PATH,
):
    """Simply opens a file and send it"""

    with open(audio_path, "rb") as file:
        response = requests.post(
            Config.BASE_URL + "/v2/upload",
            headers=Config.DEFAULT_HEADERS,
            data=file
            )

        return response.json()["upload_url"]

    raise Exception("Erro enviando arquivo para o LLM")

def send_process_status_request(audio_url: str):
    """Sends a POST request and gets transcript_id from response"""

    data = {
        "audio_url": audio_url,
        "speech_model": Config.SPEECH_MODEL,
        "speaker_labels": True
    }

    full_url = Config.BASE_URL + "/v2/transcript"

    response = requests.post(full_url, json=data, headers=Config.DEFAULT_HEADERS)

    return response.json()['id'] if not None else "Erro buscando ID da transcrição"


def transcribe_audio(
        audio_path: str = Config.AUDIO_DOWNLOAD_PATH,
        output_path: str = Config.TRANSCRITPION_PATH
        ) -> str:
    """Transcribes the audio file using AssemblyAI."""

    audio_url = upload_audio_file_to_model(audio_path=audio_path)

    process_id = send_process_status_request(audio_url=audio_url)

    polling_endpoint = Config.BASE_URL + "/v2/transcript/" + process_id

    while True:
        transcription_result = requests.get(polling_endpoint, headers=Config.DEFAULT_HEADERS).json()
        transcript_text = transcription_result['text']

        if transcription_result['status'] == 'completed':
            with open(output_path if None else Config.TRANSCRITPION_PATH , 'w', encoding='utf-8') as f:
                f.write(transcript_text)
            break

        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)












