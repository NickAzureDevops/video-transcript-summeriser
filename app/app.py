from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
import asyncio
import os
import httpx
import json

app = FastAPI()

class TranscriptRequest(BaseModel):
    transcript: str
    source: Optional[str] = None  # 'teams' or 'youtube'

class YouTubeRequest(BaseModel):
    video_id: str

async def summarize_with_foundry(transcript: str, instructions: str = "Summarize this transcript.") -> str:
    FOUNDRY_API_KEY = os.environ.get("FOUNDRY_API_KEY")
    FOUNDRY_MODEL_ID = os.environ.get("FOUNDRY_MODEL_ID")
    FOUNDRY_PROJECT_URL = os.environ.get("FOUNDRY_PROJECT_URL")
    prompt = instructions + "\n" + transcript[:4000]
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
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(request.video_id)
        transcript = " ".join([entry['text'] for entry in transcript_list])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch transcript: {str(e)}")
    summary = await summarize_with_foundry(transcript, "Summarize this YouTube transcript.")
    return {"summary": summary}
