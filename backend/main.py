"""Main FastAPI application for Karaoke Stem Separator."""

# pylint: disable=import-error
# type: ignore[reportMissingImports]

from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .utils.spleeter_utils import separate_stems


class UploadResponse(BaseModel):
    status: str
    filename: Optional[str] = None
    link: Optional[str] = None


class SeparateResponse(BaseModel):
    status: str
    files: list[str]


class KaraokeResponse(BaseModel):
    status: str


class LyricsResponse(BaseModel):
    lyrics: list[str]
    timestamps: list[str]


class VideoResponse(BaseModel):
    status: str


class MusicResponse(BaseModel):
    status: str


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=UploadResponse)
async def read_root() -> UploadResponse:
    """Root endpoint."""
    return UploadResponse(status="ok")


@app.post("/upload/", response_model=UploadResponse)
async def upload_media(
    upload_file: Optional[UploadFile] = File(None),
    link: Optional[str] = Form(None),
) -> UploadResponse:
    """Upload a media file or link for processing."""
    if upload_file is not None:
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        destination = uploads_dir / upload_file.filename
        content = await upload_file.read()
        destination.write_bytes(content)
        return UploadResponse(status="received", filename=upload_file.filename)

    if link is not None:
        return UploadResponse(status="received_link", link=link)

    raise HTTPException(status_code=400, detail="No file or link provided")


@app.post("/separate/", response_model=SeparateResponse)
async def separate_audio(
    filename: str = Form(...),
    stems: int = Form(2),
) -> SeparateResponse:
    """Separate audio stems using Spleeter."""
    uploads_dir = Path("uploads")
    input_path = uploads_dir / filename
    if not input_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    output_dir = Path("separated")
    output_dir.mkdir(exist_ok=True)
    files = separate_stems(str(input_path), str(output_dir), stems)
    return SeparateResponse(status="separated", files=files)


@app.post("/karaoke/", response_model=KaraokeResponse)
async def make_karaoke(_filename: str = Form(...)) -> KaraokeResponse:
    """Create karaoke version."""
    return KaraokeResponse(status="karaoke_ready")


@app.post("/transcribe_lyrics/", response_model=LyricsResponse)
async def transcribe_lyrics(_filename: str = Form(...)) -> LyricsResponse:
    """Transcribe lyrics and timestamps."""
    return LyricsResponse(lyrics=[], timestamps=[])


@app.post("/generate_video/", response_model=VideoResponse)
async def generate_video(_filename: str = Form(...)) -> VideoResponse:
    """Generate karaoke video."""
    return VideoResponse(status="video_ready")


@app.post("/transcribe_music/", response_model=MusicResponse)
async def transcribe_music(_filename: str = Form(...)) -> MusicResponse:
    """Transcribe music to tabs/MIDI/notation."""
    return MusicResponse(status="music_transcribed")
