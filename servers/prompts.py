def generic_summary_prompt(transcript: str) -> str:
    return f"Summarize the following transcript:\n{transcript}"

def youtube_summary_prompt(transcript: str) -> str:
    return f"Summarize this YouTube video transcript:\n{transcript}"

def teams_summary_prompt(transcript: str) -> str:
    return f"Summarize this Teams meeting transcript:\n{transcript}"