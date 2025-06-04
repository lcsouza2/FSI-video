import whisper
import pydub
from config import Config

segments = pydub.AudioSegment.from_file(file="downloaded.mp3")

chunks = [
    segments[i:i + Config.CHUNK_LENGHT_MS] 
    for i in range(0, len(segments), Config.CHUNK_LENGHT_MS)
    ]

