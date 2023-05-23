from fastapi import FastAPI, UploadFile, HTTPException, File, Depends
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from typing import List, Optional
from starlette import status
from pydantic import BaseModel
import uvicorn
import os
import whisper
from dotenv import load_dotenv

load_dotenv()

get_bearer_token = HTTPBearer(auto_error=False)
known_tokens = set([os.getenv('BearerToken')])

def transcribe_audio(file_path: str) -> str:
    model = whisper.load_model("large")
    text = model.transcribe(file_path, fp16=False)
    os.remove(file_path)
    return text

app = FastAPI(
    title='Strath-Bot API',
    version='0.1.0',
    description='Bot Service'
)

class UnauthorizedMessage(BaseModel):
    detail: str = "Bearer token missing or unknown"

@app.post("/api/v1/upload/", tags=["Speech2Text"])
async def upload_file(file: UploadFile = File(description="mp3 file"), auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)):
    if auth is None or (token := auth.credentials) not in known_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedMessage().detail,
        )
    
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
