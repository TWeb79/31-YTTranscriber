"""
Transcription service layer for YouTube video transcription.
"""

import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from yt_transcriber import transcribe_url, transcribe_chain, get_video_chain


def fetch_video_transcript(
    url: str,
    model_size: str = "base",
    languages: Optional[list] = None,
) -> dict:
    """
    Fetch transcript for a single YouTube video.

    Parameters
    ----------
    url : str
        YouTube video URL
    model_size : str
        Whisper model size (if captions unavailable)
    languages : list, optional
        Preferred caption languages

    Returns
    -------
    dict
        Transcript result with title, url, video_id, transcript, etc.
    """
    return transcribe_url(
        url=url,
        model_size=model_size,
        languages=languages,
        force_whisper=False,
    )


def fetch_video_chain(
    url: str,
    n: int = 5,
    model_size: str = "base",
    languages: Optional[list] = None,
) -> list:
    """
    Fetch transcripts for multiple videos starting from URL.

    Parameters
    ----------
    url : str
        YouTube video, playlist, or channel URL
    n : int
        Number of videos to process
    model_size : str
        Whisper model size
    languages : list, optional
        Preferred caption languages

    Returns
    -------
    list
        List of transcript result dicts
    """
    return transcribe_chain(
        url=url,
        n=n,
        model_size=model_size,
        languages=languages,
    )


def get_related_videos(url: str, n: int = 5) -> list:
    """
    Get related videos from a YouTube URL.

    Parameters
    ----------
    url : str
        YouTube video or channel URL
    n : int
        Number of videos to retrieve

    Returns
    -------
    list
        List of {"url": ..., "title": ...} dicts
    """
    return get_video_chain(url=url, n=n)


def list_transcripts() -> list:
    """
    List all saved transcripts.

    Returns
    -------
    list
        List of transcript file info
    """
    transcripts_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "transcripts"
    )
    if not os.path.exists(transcripts_dir):
        return []

    files = []
    for filename in os.listdir(transcripts_dir):
        if filename.startswith("transcript_") and filename.endswith(".md"):
            filepath = os.path.join(transcripts_dir, filename)
            files.append({
                "filename": filename,
                "path": filepath,
                "size": os.path.getsize(filepath),
            })
    return files
