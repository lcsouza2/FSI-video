from yt_dlp import YoutubeDL
from core.config import Config
import whisper

ydl_opts = {
    'format': Config.AUDIO_FORMAT,
    'outtmpl': Config.AUDIO_DOWNLOAD_PATH,
    'postprocessors': Config.POST_PROCESSORS,
    'ffmpeg_location': Config.FFMPEG_PATH, 
}

def format_video_url(video_url: str) -> str:
    return video_url.strip()


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

    video_url = format_video_url(video_url)

    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
            return ydl.prepare_filename(ydl.extract_info(video_url, download=False))
        except Exception as e:
            print(f"Error downloading: {e}")
            return ""

def transcribe_audio(
        audio_path: str = Config.AUDIO_DOWNLOAD_PATH,
        output_path: str = Config.TRANSCRITPION_PATH
        ) -> str:
    """
    Transcribes the audio file using Whisper.
    Returns:
        str: File path with the transcribe result.
    """
    model = whisper.load_model(Config.WHISPER_MODEL)
    result = model.transcribe(audio=audio_path)

    with open(Config.TRANSCRITPION_PATH, 'w', encoding='utf-8') as f:
        f.write(result['text'])

    return output_path