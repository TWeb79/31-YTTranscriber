"""
API routes for YouTube Transcriber.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel

from services.transcriber import (
    fetch_video_transcript,
    fetch_video_chain,
    get_related_videos,
    list_transcripts,
)


router = APIRouter(prefix="/api", tags=["transcriber"])


class TranscriptRequest(BaseModel):
    """Request model for single video transcription."""
    url: str
    model_size: str = "base"
    languages: Optional[list[str]] = None


class ChainRequest(BaseModel):
    """Request model for video chain transcription."""
    url: str
    n: int = 5
    model_size: str = "base"
    languages: Optional[list[str]] = None


class VideoChainRequest(BaseModel):
    """Request model for getting related videos."""
    url: str
    n: int = 5


@router.post("/transcribe")
async def transcribe_video(request: TranscriptRequest) -> dict:
    """
    Transcribe a single YouTube video.

    Returns transcript with title, url, video_id, transcript text, etc.
    """
    result = fetch_video_transcript(
        url=request.url,
        model_size=request.model_size,
        languages=request.languages,
    )
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/transcribe-chain")
async def transcribe_video_chain(request: ChainRequest) -> list:
    """
    Transcribe multiple videos from a YouTube URL.

    Handles playlists, channels, or single videos.
    """
    results = fetch_video_chain(
        url=request.url,
        n=request.n,
        model_size=request.model_size,
        languages=request.languages,
    )
    return results


@router.get("/videos")
async def get_videos(url: str = Query(...), n: int = Query(5)) -> list:
    """
    Get related videos from a YouTube URL.

    Query parameters:
    - url: YouTube video or channel URL
    - n: Number of videos to retrieve (default: 5)
    """
    return get_related_videos(url=url, n=n)


@router.get("/transcripts")
async def get_transcripts() -> list:
    """
    List all saved transcripts.
    """
    return list_transcripts()


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "yt-transcriber"}
