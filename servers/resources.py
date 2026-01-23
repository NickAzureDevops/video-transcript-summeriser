YOUTUBE_TRANSCRIPTS = {}
TEAMS_TRANSCRIPTS = {}

def cache_youtube_transcript(video_id: str, transcript: str):
    YOUTUBE_TRANSCRIPTS[video_id] = transcript

def cache_teams_transcript(meeting_id: str, transcript: str):
    TEAMS_TRANSCRIPTS[meeting_id] = transcript
