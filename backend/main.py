"""Main FastAPI application for Karaoke Stem Separator."""
# type: ignore[reportMissingImports]

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .utils.spleeter_utils import separate_stems


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Karaoke Stem Separator API"}


@app.post("/upload/")
async def upload_media(
    upload_file: Annotated[Optional[UploadFile], File(None)],
    link: Annotated[Optional[str], Form(None)],
) -> dict[str, str]:
    """Upload a media file or link for processing."""
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)

    if upload_file is not None:
        file_path = uploads_dir / upload_file.filename
        content = await upload_file.read()
        file_path.write_bytes(content)
        return {"status": "received", "filename": upload_file.filename}

    if link is not None:
        assert isinstance(link, str)
        return {"status": "received_link", "link": link}

    raise HTTPException(status_code=400, detail="No file or link provided")


@app.post("/separate/")
async def separate_audio(
    filename: Annotated[str, Form(...)],
    stems: Annotated[int, Form(2)],
) -> dict[str, str | list[str]]:
    """Separate audio stems using Spleeter."""
    uploads_dir = Path("uploads")
    input_file = uploads_dir / filename
    if not input_file.exists():
        raise HTTPException(status_code=404, detail="File not found")

    separated_dir = Path("separated")
    separated_dir.mkdir(exist_ok=True)
    files = separate_stems(str(input_file), str(separated_dir), stems)
    return {"status": "separated", "files": files}


@app.post("/karaoke/")
async def make_karaoke(
    _filename: Annotated[str, Form(...)],
) -> dict[str, str]:
    """Create karaoke version."""
    # Placeholder logic
    return {"status": "karaoke_ready"}


@app.post("/transcribe_lyrics/")
async def transcribe_lyrics(
    _filename: Annotated[str, Form(...)],
) -> dict[str, list[str]]:
    """Transcribe lyrics and timestamps."""
    # Placeholder logic
    return {"lyrics": [], "timestamps": []}


@app.post("/generate_video/")
async def generate_video(
    _filename: Annotated[str, Form(...)],
) -> dict[str, str]:
    """Generate karaoke video."""
    # Placeholder logic
    return {"status": "video_ready"}


@app.post("/transcribe_music/")
async def transcribe_music(
    _filename: Annotated[str, Form(...)],
) -> dict[str, str]:
    """Transcribe music to tabs/MIDI/notation."""
    # Placeholder logic
    return {"status": "music_transcribed"}
