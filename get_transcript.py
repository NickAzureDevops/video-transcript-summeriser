"""Print a YouTube transcript as plain text (translated to English when needed).

Used by the GitHub agentic workflow (and handy locally): the agent runs this
to fetch captions, then writes the summary or translation itself.

The script always tries to return an English transcript. If the video has no
English captions it falls back to the first available transcript and translates
it to English via the YouTube transcript-translation API.

Usage:
    python3 get_transcript.py "https://www.youtube.com/watch?v=4MUgq_rzjqo"
"""
import re
import sys

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound


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
    """Fetch captions as clean, joined English text.

    Preference order:
    1. An existing English transcript (manual or auto-generated).
    2. Any available transcript translated to English via the YouTube API.
    """
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    try:
        transcript = transcript_list.find_transcript(["en"])
    except NoTranscriptFound:
        # No English captions — grab the first available one and translate it.
        transcript = next(iter(transcript_list))
        if transcript.is_translatable:
            transcript = transcript.translate("en")
        else:
            print(
                f"Warning: no English transcript available and '{transcript.language}' "
                "transcript is not translatable. Using original language transcript.",
                file=sys.stderr,
            )

    fetched = transcript.fetch()
    return " ".join(s.text.strip() for s in fetched if s.text.strip())


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    print(get_transcript(extract_video_id(sys.argv[1])))


if __name__ == "__main__":
    main()
