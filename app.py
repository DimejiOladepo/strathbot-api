from fastapi import FastAPI, UploadFile, HTTPException, File, Depends
from fastapi.openapi.utils import get_openapi
from typing import List
import uvicorn
import os
import whisper

def transcribe_audio(file_path: str) -> str:
    model = whisper.load_model("large")
    text = model.transcribe(file_path, fp16=False)
    os.remove(file_path)
    return text

app = FastAPI(
    title='Strath-bot API',
    version='0.1.0',
    description='Audio Processing Service'
)

@app.post("/api/v1/upload/", tags=["Speech2Text"])
async def upload_file(file: UploadFile = File(description="mp3 file")):

    # Check file size
    if file.content_type != "audio/mpeg" or len(await file.read()) >= 5242880:
        raise HTTPException(status_code=400, detail="Invalid file format or size")

    # Save the uploaded file
    with open(file.filename, "wb") as f:
        f.write(await file.read())

    # Transcribe the audio file
    transcription = transcribe_audio(file.filename)

    # Return the transcription result
    return {"transcription": transcription}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7070)
