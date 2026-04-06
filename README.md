# YouTube Transcriber

Fetches transcripts from YouTube videos and saves them as Markdown files.

## Requirements

```bash
pip install youtube-transcript-api yt-dlp
```

## Usage

```bash
python yt_transcriber.py <url> [n] [model_size]

example: python yt_transcriber.py "https://www.youtube.com/watch?v=DPmtnb8NBog" 2   

```
  
### Parameters

- `url` - YouTube video or playlist URL
- `n` - number of videos to process (default: 1)
- `model_size` - whisper model size (default: base)

### Examples

```bash
# Single video
python yt_transcriber.py "https://www.youtube.com/watch?v=uAH7C9Z40UY"

# Multiple videos from a channel
python yt_transcriber.py "https://www.youtube.com/watch?v=uAH7C9Z40UY" 5

# Playlist
python yt_transcriber.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" 10
```

## Output

Transcripts are saved to the `transcripts/` folder as `transcript_<VIDEO_ID>.md` files.

## Web UI and Docker

This repository now includes a minimal FastAPI-based web UI and a Docker setup.

Service ports (per RULES_ports.md):

- FastAPI API: 8130 (project 30 → 81NN pattern)

Run locally with Python:

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8130
```

Or with Docker:

```bash
docker compose up --build
# then open http://localhost:8130 in your browser
```

## Features

- Fast caption extraction via YouTube's native captions
- Supports playlists and channel video extraction
- Automatic retry with related videos from channel
- Saves transcripts as Markdown with title heading