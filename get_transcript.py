"""Print a YouTube transcript as plain text.

Used by the GitHub agentic workflow (and handy locally): the agent runs this
to fetch captions, then writes the summary itself.

Usage:
    python3 get_transcript.py "https://www.youtube.com/watch?v=4MUgq_rzjqo"
"""
import re
import sys

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """Pull the 11-char video id out of any common YouTube URL form (or a bare id)."""
    patterns = [
        r"(?:v=|/shorts/|/embed/|/live/|youtu\.be/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not find a YouTube video id in: {url}")


def get_transcript(video_id: str) -> str:
    """Fetch the captions as clean, joined text."""
    fetched = YouTubeTranscriptApi().fetch(video_id)
    return " ".join(s.text.strip() for s in fetched if s.text.strip())


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    print(get_transcript(extract_video_id(sys.argv[1])))


if __name__ == "__main__":
    main()
