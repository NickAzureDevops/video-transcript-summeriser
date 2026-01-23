# MCP Server for YouTube & Teams Transcript Summarization

## Endpoints
- `/summarize/youtube`: Summarize YouTube video transcript by video ID
- `/summarize/upload`: Upload transcript file for summarization (works for Teams, YouTube, or any transcript)
- `/summarize`: Paste transcript text for summarization (works for Teams, YouTube, or any transcript)

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Start the server: `uvicorn app.app:app --reload`
3. POST YouTube video ID, upload transcript file, or paste transcript text to endpoints

## Teams Support
- Manual upload or paste of Teams transcripts is supported (works for free Teams accounts).
- Automatic fetching of Teams transcripts via API requires paid/enterprise Teams and extra setup.

## Foundry Integration
- Summarization is performed using a Microsoft Foundry agent (see `app/app.py`).
- Set your Foundry project endpoint and model deployment name in the code.

## Example YouTube Request
```json
{
  "video_id": "YOUTUBE_VIDEO_ID"
}
```
