from datetime import timedelta
from pyannote.core import Segment

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
