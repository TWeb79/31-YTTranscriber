# YouTube Transcriber

Fetches transcripts from YouTube videos and saves them as Markdown files.

## Requirements

```bash
pip install youtube-transcript-api yt-dlp
```

## Usage

```bash
python yt_transcriber.py <url> [n] [model_size]
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

## Features

- Fast caption extraction via YouTube's native captions
- Supports playlists and channel video extraction
- Automatic retry with related videos from channel
- Saves transcripts as Markdown with title heading