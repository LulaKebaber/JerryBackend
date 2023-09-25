from fastapi import Depends, status, File, UploadFile, HTTPException, FastAPI
# from ..models import Transcription
# from datetime import datetime
from ..service import Service, get_service
from ..service_gpt import ask_gpt
from . import router

from dotenv import load_dotenv
import os
import requests

load_dotenv()

@router.post("/users/transcriptions", status_code=status.HTTP_201_CREATED)
def transcribe_audio(
    file: UploadFile = File(...),
    svc: Service = Depends(get_service),
):
    # Make sure we're at the start of the file
    file.file.seek(0)

    api_token = "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"
    
    # Transcribe the audio file using OpenAI's Whisper ASR API
    response = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers={
            "Authorization": f"Bearer {api_token}",
        },
        files={"file": (file.filename, file.file)},  # Corrected here
        data={"model": "whisper-1"},
    )

    # Check the status of the request
    if response.status_code != 200:
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.json()}")
        raise HTTPException(status_code=400, detail="Transcription failed")

    # Get the transcription from the response
    data = response.json()
    data = ask_gpt(data["text"])

    return data