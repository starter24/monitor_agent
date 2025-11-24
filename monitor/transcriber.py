import whisper
import os

# Load the model once (base model for speed)
model = whisper.load_model("base")

def transcribe_audio(file_path):
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Transcription error: {e}")
        return "[Error] Failed to transcribe audio."
