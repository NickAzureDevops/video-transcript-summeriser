from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP
from tools import summarize_transcript, fetch_youtube_transcript, summarize_youtube_video, summarize_teams_transcript
from resources import YOUTUBE_TRANSCRIPTS, TEAMS_TRANSCRIPTS
from prompts import generic_summary_prompt, youtube_summary_prompt, teams_summary_prompt
import os
import re

app = FastAPI()

# --- FastAPI endpoint for YouTube video summarization ---
@app.post("/summarize_youtube")
async def summarize_youtube_http(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return JSONResponse({"error": "Missing 'url' in request."}, status_code=400)
    summary = await summarize_youtube_video(url)
    return JSONResponse({"summary": summary})

mcp = FastMCP("transcript-mcp-server", host="0.0.0.0", port=8000)

@mcp.tool()
async def summarize(transcript: str, source: str = "generic") -> str:
    """Summarize a transcript from any source."""
    return await summarize_transcript(transcript, source)

@mcp.tool()
async def fetch_youtube(video_id: str) -> str:
    """Fetch transcript for a YouTube video."""
    return await fetch_youtube_transcript(video_id)

@mcp.tool()
async def summarize_youtube_video_tool(url: str) -> str:
    return await summarize_youtube_video(url)
@mcp.tool()
async def summarize_teams(transcript: str) -> str:
    """Summarize a Teams meeting transcript."""
    return await summarize_teams_transcript(transcript)

@mcp.resource("transcript://youtube")
def get_youtube_transcripts() -> str:
    import json
    return json.dumps(YOUTUBE_TRANSCRIPTS)

@mcp.resource("transcript://teams")
def get_teams_transcripts() -> str:
    import json
    return json.dumps(TEAMS_TRANSCRIPTS)

@mcp.prompt()
def generic_prompt(transcript: str) -> str:
    return generic_summary_prompt(transcript)

@mcp.prompt()
def youtube_prompt(transcript: str) -> str:
    return youtube_summary_prompt(transcript)

@mcp.prompt()
def teams_prompt(transcript: str) -> str:
    return teams_summary_prompt(transcript)
