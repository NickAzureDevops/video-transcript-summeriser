from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from servers.tools import summarize_youtube_video, summarize_transcript

app = FastAPI()

class TranscriptRequest(BaseModel):
    transcript: str
    source: Optional[str] = None  # 'teams' or 'youtube'

class YouTubeRequest(BaseModel):
    video_id: str

@app.post("/summarize")
async def summarize_transcript(request: TranscriptRequest):
    summary = await summarize_transcript(request.transcript, request.source or "unknown")
    return {"summary": summary}

@app.post("/summarize/upload")
async def summarize_transcript_upload(file: UploadFile = File(...), source: Optional[str] = None):
    content = await file.read()
    transcript = content.decode("utf-8")
    summary = await summarize_transcript(transcript, source or "unknown")
    return {"summary": summary}

@app.post("/summarize/youtube")
async def summarize_youtube(request: YouTubeRequest):
    video_id = request.video_id
    if not video_id:
        raise HTTPException(status_code=400, detail="No valid YouTube video ID provided.")
    summary = await summarize_youtube_video(video_id)
    return {"summary": summary}

