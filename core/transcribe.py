import whisper
from pyannote.audio import Pipeline
from utils import timestamp_to_seconds
from typing import List, Dict
import re
import json

def transcribe_audio(file):
    model = whisper.load_model("base")
    result = model.transcribe(file)
    return result

def recognize_speakers(file):
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization@2.1",
        use_auth_token="tá no drive olha lá"
    )
    diarization = pipeline(file)


    pattern = re.compile(
        r"\[\s*([\d:.]+)\s*-->\s*([\d:.]+)\s*\]\s*\w+\s+(SPEAKER_\d+)"
    )

    result = []
    for match in pattern.finditer(diarization):
        start_ts, end_ts, speaker = match.groups()
        start = timestamp_to_seconds(start_ts)
        end = timestamp_to_seconds(end_ts)
        result.append({
            "start": round(start, 3),
            "end": round(end, 3),
            "speaker": speaker
        })

    return result

def assign_speakers_to_segments(
    whisper_segments: List[Dict],
    diarized_segments: List[Dict]
    ) -> List[Dict]:

    final_output = []

    for segment in whisper_segments["segments"]:
        whisper_start = segment["start"]
        whisper_end = segment["end"]
        whisper_text = segment["text"]

        # Inicializa
        chosen_speaker = "UNKNOWN"
        max_overlap = 0.0

        for diar in diarized_segments:
            diar_start = diar["start"]
            diar_end = diar["end"]
            diar_speaker = diar["speaker"]

            # Calcula interseção
            latest_start = max(whisper_start, diar_start)
            earliest_end = min(whisper_end, diar_end)
            overlap = max(0.0, earliest_end - latest_start)

            if overlap > max_overlap:
                max_overlap = overlap
                chosen_speaker = diar_speaker

        # Salva a transcrição com o speaker atribuído
        final_output.append({
            "start": whisper_start,
            "end": whisper_end,
            "speaker": chosen_speaker,
            "text": whisper_text
        })

    return final_output


print(assign_speakers_to_segments())
