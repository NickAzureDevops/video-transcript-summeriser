from fastapi import FastAPI, Request, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import re
from servers.tools import summarize_youtube_video

app = FastAPI()

class TranscriptRequest(BaseModel):
    transcript: str
    source: Optional[str] = None  # 'teams' or 'youtube'

class YouTubeRequest(BaseModel):
    video_id: str

@app.post("/summarize")
async def summarize_transcript(request: TranscriptRequest):
    # Placeholder for actual summarization logic
    summary = f"Summary of {request.source or 'unknown'} transcript: {request.transcript[:100]}..."
    return {"summary": summary}

@app.post("/summarize/upload")
async def summarize_transcript_upload(file: UploadFile = File(...), source: Optional[str] = None):
    content = await file.read()
    transcript = content.decode("utf-8")
    summary = f"Summary of {source or 'unknown'} transcript: {transcript[:100]}..."
    return {"summary": summary}

@app.post("/summarize/youtube")
async def summarize_youtube(request: YouTubeRequest):
    video_id = request.video_id
    if not video_id:
        raise HTTPException(status_code=400, detail="No valid YouTube video ID provided.")
    summary = await summarize_youtube_video(video_id)
    return {"summary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("servers.api:app", host="0.0.0.0", port=8080, log_level="info")
