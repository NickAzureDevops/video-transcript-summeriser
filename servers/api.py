from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Optional
from servers.tools import summarize_youtube_video, summarize_transcript
from servers.youtube_captions import download_caption

app = FastAPI()

class TranscriptRequest(BaseModel):
    transcript: str
    source: Optional[str] = None  # 'teams' or 'youtube'
    length: Optional[str] = "medium"  # 'short', 'medium', 'long'
    style: Optional[str] = "paragraph"  # 'paragraph', 'bullets', 'actions'

class YouTubeRequest(BaseModel):
    video_id: str

class CaptionDownloadRequest(BaseModel):
    caption_id: str
    tfmt: str = "srt"  # 'srt' or 'vtt'
@app.post("/youtube/captions/download", response_class=PlainTextResponse)
async def youtube_caption_download(request: CaptionDownloadRequest):
    try:
        caption_text = download_caption(request.caption_id, request.tfmt)
        return caption_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize_transcript_endpoint(request: TranscriptRequest):
    summary = await summarize_transcript(
        request.transcript,
        request.source or "unknown",
        request.length or "medium",
        request.style or "paragraph"
    )
    return {"summary": summary}

@app.post("/summarize/upload")
async def summarize_transcript_upload(
    file: UploadFile = File(...),
    source: Optional[str] = None,
    length: Optional[str] = "medium",
    style: Optional[str] = "paragraph"
):
    content = await file.read()
    transcript = content.decode("utf-8")
    summary = await summarize_transcript(
        transcript,
        source or "unknown",
        length or "medium",
        style or "paragraph"
    )
    return {"summary": summary}

@app.post("/summarize/youtube")
async def summarize_youtube(request: YouTubeRequest):
    video_id = request.video_id
    if not video_id:
        raise HTTPException(status_code=400, detail="No valid YouTube video ID provided.")
    summary = await summarize_youtube_video(video_id)
    return {"summary": summary}

