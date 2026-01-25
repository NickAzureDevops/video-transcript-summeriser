from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
app = FastAPI()

class TranscriptRequest(BaseModel):
    transcript: str
    source: Optional[str] = None

class YouTubeRequest(BaseModel):
    video_id: str

class YouTubeUrlRequest(BaseModel):
    url: str

def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu.be/)([\w-]{11})", url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)

async def summarize_with_foundry(transcript: str, instructions: str = "Summarize this transcript.") -> str:
    MODEL_DEPLOYMENT_NAME = os.environ.get("MODEL_DEPLOYMENT_NAME")
    OPENAI_ENDPOINT = os.environ.get("FOUNDRY_PROJECT_URL")
    OPENAI_API_KEY = os.environ.get("FOUNDRY_API_KEY")
    prompt = instructions + "\n" + transcript[:4000]
    client = OpenAI(
        base_url=OPENAI_ENDPOINT,
        api_key=OPENAI_API_KEY
    )
    response = client.chat.completions.create(
        model=MODEL_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
            {"role": "user", "content": prompt}
        ],
    )
    return {"summary": response.choices[0].message.content.strip()}

@app.post("/summarize")
async def summarize_transcript(request: TranscriptRequest):
    summary = await summarize_with_foundry(request.transcript, f"Summarize this {request.source or 'unknown'} transcript.")
    return {"summary": summary}

@app.post("/summarize/upload")
async def summarize_transcript_upload(file: UploadFile = File(...), source: Optional[str] = None):
    content = await file.read()
    transcript = content.decode("utf-8")
    summary = await summarize_with_foundry(transcript, f"Summarize this {source or 'unknown'} transcript.")
    return {"summary": summary}

@app.post("/summarize/youtube")
async def summarize_youtube(request: YouTubeRequest):
    transcripts = YouTubeTranscriptApi.list_transcripts(request.video_id)
    transcript_obj = transcripts.find_transcript(['en'])
    transcript_list = transcript_obj.fetch()
    transcript = " ".join([entry['text'] for entry in transcript_list])
    result = await summarize_with_foundry(transcript, "Summarize this YouTube transcript.")
    return result

@app.post("/summarize_youtube")
async def summarize_youtube_legacy(request: YouTubeUrlRequest):
    video_id = extract_video_id(request.url)
    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript_obj = transcripts.find_transcript(['en'])
    transcript_list = transcript_obj.fetch()
    transcript = " ".join([entry['text'] for entry in transcript_list])
    summary = await summarize_with_foundry(transcript, "Summarize this YouTube transcript.")
    return {"summary": summary}
