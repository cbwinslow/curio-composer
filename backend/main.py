from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from utils.spleeter_utils import separate_stems as spleeter_separate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Karaoke Stem Separator API"}

# Placeholder endpoints for MVP
@app.post("/upload/")
async def upload_media(file: UploadFile = File(...), link: Optional[str] = Form(None)):
    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    if file:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        return {"status": "received", "filename": file.filename}
    elif link:
        return {"status": "received_link", "link": link}
    else:
        raise HTTPException(status_code=400, detail="No file or link provided")

@app.post("/separate/")
async def separate_stems(filename: str = Form(...), stems: int = Form(2)):
    input_filepath = os.path.join("uploads", filename)
    if not os.path.exists(input_filepath):
        raise HTTPException(status_code=404, detail="File not found")
    output_dir = "separated"
    os.makedirs(output_dir, exist_ok=True)
    files = spleeter_separate(input_filepath, output_dir, stems)
    return {"status": "separated", "files": files}

@app.post("/karaoke/")
async def make_karaoke(filename: str):
    # Remove vocals, modify music
    return {"status": "karaoke_ready"}

@app.post("/transcribe_lyrics/")
async def transcribe_lyrics(filename: str):
    # Call lyrics transcriber
    return {"lyrics": [], "timestamps": []}

@app.post("/generate_video/")
async def generate_video(filename: str):
    # Generate karaoke video
    return {"status": "video_ready"}

@app.post("/transcribe_music/")
async def transcribe_music(filename: str):
    # Transcribe to tabs/MIDI/notation
    return {"status": "music_transcribed"}
