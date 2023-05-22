import whisper, os

def transcribe_audio(file_path: str) -> str:
    model = whisper.load_model("large")
    text = model.transcribe(file_path, fp16=False)
    os.remove(file_path)
    return text

transcribe_audio("Audio.mp3")