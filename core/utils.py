import pydub
from core.config import Config

def segment_audio(
        audio_path: str = "static/audio.mp3", 
        chunk_length_ms: int = Config.CHUNK_LENGHT_MS
        ) -> list:
    """
    Segments an audio file into chunks of specified length.
    """
    segments = pydub.AudioSegment.from_file(audio_path)

    chunks = [
        segments[i:i + chunk_length_ms] 
        for i in range(0, len(segments), chunk_length_ms)
    ]

    return chunks