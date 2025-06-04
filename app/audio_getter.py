from yt_dlp import YoutubeDL
from config import Config

ydl_opts = {
'format': Config.AUDIO_FORMAT,
'outtmpl': Config.TARGET_DOWNLOAD_PATH,
'postprocessors': Config.POST_PROCESSORS,
'ffmpeg_location': Config.FFMPEG_PATH, 
}

def format_video_url(video_url: str) -> str:
    return video_url.strip()


def download_audio(video_url: str) -> str:
    """
    Downloads the audio from the given video URL using yt-dlp.

    Returns:
        str: The path to the downloaded audio file.
    """

    video_url = format_video_url(video_url)

    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
            return ydl.prepare_filename(ydl.extract_info(video_url, download=False))
        except Exception as e:
            print(f"Error downloading: {e}")
            return ""