# Karaoke Stem Separator Web App

## Features
- Upload audio/video or provide a link
- Separate stems (vocals, accompaniment, etc.)
- Remove vocals, modify music for karaoke
- Transcribe lyrics (LLM, timestamped)
- Generate karaoke video/slideshow
- Transcribe music to tabs/MIDI/notation
- Save, share, and modify music

## Tech Stack
- **Frontend:** React
- **Backend:** FastAPI (Python), Spleeter, ffmpeg, music21, LLMs

## Quickstart
- Backend:
  ```bash
  cd backend
  python3 -m pip install -r requirements.txt
  python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```
- Frontend:
  ```bash
  cd frontend && npm install && npm start
  ```
