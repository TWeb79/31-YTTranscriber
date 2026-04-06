from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

# Import existing transcriber module from repository root
import yt_transcriber as yt

app = FastAPI(title="YT Transcriber API")

# Allow the frontend served from same compose network to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Serve the static frontend files if present
static_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


@app.get("/api/health")
def health() -> JSONResponse:
    """Simple health endpoint."""
    return JSONResponse({"status": "ok"})


@app.get("/api/transcribe")
def api_transcribe(url: str, n: Optional[int] = 1) -> JSONResponse:
    """Transcribe a single URL or a chain of videos.

    - If n == 1: returns a single transcribe_url() result.
    - If n > 1: returns a list from transcribe_chain().
    """
    if not url:
        raise HTTPException(status_code=400, detail="url parameter is required")

    try:
        if n <= 1:
            result = yt.transcribe_url(url)
            return JSONResponse(result)
        else:
            results = yt.transcribe_chain(url, n=n)
            return JSONResponse({"results": results})
    except Exception as exc:  # pragma: no cover - surface errors to client
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/available")
def api_available() -> JSONResponse:
    """Report which optional dependencies are present.

    This helps developers know if the fast-path (youtube-transcript-api)
    or metadata extraction (yt-dlp) are available in the container.
    """
    deps = {
        "youtube_transcript_api": _is_importable("youtube_transcript_api"),
        "yt_dlp": _is_importable("yt_dlp"),
    }
    return JSONResponse(deps)


def _is_importable(name: str) -> bool:
    try:
        __import__(name)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    # Run with Uvicorn when invoked directly for local debugging
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8130, log_level="info")
