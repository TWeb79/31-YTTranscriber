# Architecture Overview

This repository provides a small YouTube transcription utility with a minimal web UI.

Components

- yt_transcriber.py: Core transcription logic. Extracts video IDs, fetches native YouTube captions via youtube-transcript-api or collects metadata via yt-dlp. Produces markdown transcript files in transcripts/.
- app/main.py: FastAPI wrapper exposing endpoints for transcribing (GET /api/transcribe) and reporting available optional dependencies. Serves static frontend located at app/frontend/.
- app/frontend/index.html: Minimal single-file frontend calling the API.
- Dockerfile / docker-compose.yml: Containerized deployment for local development. The FastAPI service listens on port 8130 (per RULES_ports.md layout for project 30 → 81NN).
- tests/: unit tests for core utilities.

Data Flow

Frontend -> FastAPI (/api/transcribe) -> yt_transcriber -> returns result -> frontend displays transcript.

Design notes

- Business logic remains in yt_transcriber.py; app/main.py is thin routing and orchestration.
- Dependencies that enable fast/metadata paths are optional and checked at runtime. This keeps the container lightweight when not needed.
- Files are intentionally small and modular to follow RULES_coding.md.
