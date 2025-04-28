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
- `cd backend && pip install -r requirements.txt && uvicorn main:app --reload`
- `cd frontend && npm install && npm start`
