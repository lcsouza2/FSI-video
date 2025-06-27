from datetime import timedelta
from pyannote.core import Segment
from core.config import Config
from google.genai import types
from google import genai

def assign_speakers_to_transcript(whisper_result, diarization):
    diarized_transcript = []

    for segment in whisper_result["segments"]:
        whisper_start = segment["start"]
        whisper_end = segment["end"]
        whisper_text = segment["text"]

        whisper_segment = Segment(whisper_start, whisper_end)

        speakers = diarization.crop(whisper_segment, mode="intersection")

        speaker = "UNKNOWN"
        max_overlap = 0.0
        for turn, track_speaker in speakers.itertracks(yield_label=True):
            overlap = whisper_segment & turn  # operador & retorna interseção
            if overlap.duration > max_overlap:
                max_overlap = overlap.duration
                speaker = track_speaker

        diarized_transcript.append({
            "start": whisper_start,
            "end": whisper_end,
            "speaker": speaker,
            "text": whisper_text
        })

    return diarized_transcript

def get_total_time(diarized_transcript):
    total_time = timedelta()
    for segment in diarized_transcript:
        start = segment["start"]
        end = segment["end"]
        total_time += timedelta(seconds=end - start)
    return total_time

def remove_stop_words(text):
    client = genai.Client(api_key=Config.GENAI_API_KEY)

    result = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
        "Can you remove stop words, articles, commas, dots and etc from the following text please? return only the text: " + text
        ],
        config=types.GenerateContentConfig(
            candidate_count=1,
            stop_sequences=[]
        )
    )

    return result.candidates[0].content.parts[0].text

def get_interest_points(text):
    client = genai.Client(api_key=Config.GENAI_API_KEY)

    result = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
        "Can you get interest points from this text? return like @point: ...;" + text
        ],
        config=types.GenerateContentConfig(
            candidate_count=1,
            stop_sequences=[]
        )
    )

    return result.candidates[0].content.parts[0].text