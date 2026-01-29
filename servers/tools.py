from youtube_transcript_api import YouTubeTranscriptApi
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

FOUNDRY_API_KEY = os.getenv("FOUNDRY_API_KEY", "your-foundry-api-key-here")
FOUNDRY_MODEL_ID = os.getenv("FOUNDRY_MODEL_ID", "summarization-model-id")
FOUNDRY_PROJECT_URL = os.getenv("FOUNDRY_PROJECT_URL")

openai_client = OpenAI(
    base_url=FOUNDRY_PROJECT_URL,
    api_key=FOUNDRY_API_KEY
)

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL")

async def summarize_transcript(transcript: str, source: str = "generic", length: str = "medium", style: str = "paragraph") -> str:
    # Map length to instructions
    length_map = {
        "short": "in 2 sentences",
        "medium": "in 5 sentences",
        "long": "in a detailed paragraph"
    }
    style_map = {
        "paragraph": "as a concise paragraph",
        "bullets": "as bullet points",
        "actions": "focusing on action items only"
    }
    length_instruction = length_map.get(length, "in 5 sentences")
    style_instruction = style_map.get(style, "as a concise paragraph")
    prompt = f"Summarize this {source} transcript {length_instruction} {style_instruction}:\n{transcript[:4000]}"
    response = openai_client.chat.completions.create(
        model=FOUNDRY_MODEL_ID,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=256
    )
    return response.choices[0].message.content.strip()

async def fetch_youtube_transcript(video_id: str) -> str:
    try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['en'])
        return " ".join([snippet.text for snippet in transcript_list])
    except Exception as e:
        print(f"Error fetching transcript for video_id {video_id}: {e}")
        raise

async def summarize_youtube_video(url: str) -> str:
    video_id = extract_video_id(url)
    transcript = await fetch_youtube_transcript(video_id)
    return await summarize_transcript(transcript, source="youtube")

async def summarize_teams_transcript(transcript: str) -> str:
    return await summarize_transcript(transcript, source="teams")