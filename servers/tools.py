from youtube_transcript_api import YouTubeTranscriptApi
import re

async def summarize_transcript(transcript: str, source: str = "generic") -> str:
    import os
    import httpx
    import json
    FOUNDRY_API_KEY = os.getenv("FOUNDRY_API_KEY", "your-foundry-api-key-here")
    FOUNDRY_MODEL_ID = os.getenv("FOUNDRY_MODEL_ID", "summarization-model-id")
    FOUNDRY_PROJECT_URL = os.getenv("FOUNDRY_PROJECT_URL")
    prompt = f"Summarize this {source} transcript in 5 sentences:\n{transcript[:4000]}"
    headers = {
        "Authorization": f"Bearer {FOUNDRY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": FOUNDRY_MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 256
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FOUNDRY_PROJECT_URL}/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

async def fetch_youtube_transcript(video_id: str) -> str:
    youtube_api = YouTubeTranscriptApi()
    transcript = youtube_api.get_transcript(video_id)
    return " ".join([snippet["text"] for snippet in transcript])

async def summarize_youtube_video(url: str) -> str:
    video_id = extract_video_id(url)
    transcript = await fetch_youtube_transcript(video_id)
    return await summarize_transcript(transcript, source="youtube")

async def summarize_teams_transcript(transcript: str) -> str:
    return await summarize_transcript(transcript, source="teams")