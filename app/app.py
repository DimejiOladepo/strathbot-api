from fastapi import FastAPI, UploadFile, HTTPException, File, Depends
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from typing import List, Optional
from starlette import status
from faster_whisper import WhisperModel
from pydantic import BaseModel
import uvicorn
import os
import whisper
from dotenv import load_dotenv

load_dotenv()



get_bearer_token = HTTPBearer(auto_error=False)
known_tokens = set([os.getenv('BearerToken')])

# Use Faster-whisper for much better speed compared to whisper tiny
def transcribe_audio(file_path: str, beam_size=5) -> str:
    model_size = "tiny"
    #run on CPU with INT8
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(file_path, beam_size= beam_size)
    for segment in segments:
        yield segment.text

app = FastAPI(
    title='Strath-Bot API',
    version='0.1.0',
    description='Bot Service'
)

class UnauthorizedMessage(BaseModel):
    detail: str = "Bearer token missing or unknown"


    
@app.post("/api/v1/upload/", tags=["Speech2Text"])
async def upload(file: UploadFile = File(description="mp3 file"), auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)):
    if auth is None or (token := auth.credentials) not in known_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedMessage().detail,
        )
    
    

    if "audio" in file.content_type and len(await file.read()) <= 5242880:
        audio_source = "audio_source." + file.filename[-3:]
        audio_content = await file.read()
        open(audio_source, "wb").write(audio_content)
        transcription = transcribe_audio(audio_source)
        for text in transcription:
            return(text)
        os.remove(audio_source)
        
    else:
        raise HTTPException(status_code=400, detail="Invalid file format or size")
    

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7070)
