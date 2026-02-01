# TranscriptGist: AI-Powered Transcript Summarizer

Summarizing YouTube and Teams meeting transcripts using Microsoft Foundry (OpenAI) models.

## Features
- Summarize YouTube video transcripts by video ID
- Summarize Teams or generic transcripts via file upload or pasted text
- Powered by Microsoft Foundry/OpenAI endpoints
- Simple REST API, easy to run locally or deploy

## Endpoints
* `/summarize/youtube`: Summarize YouTube video transcript by video ID
* `/summarize/upload`: Upload transcript file for summarization (works for Teams, YouTube, or any transcript)
* `/summarize`: Paste transcript text for summarization (works for Teams, YouTube, or any transcript)
* `/tools`: Chat with available tools by specifying tool name and parameters (see below)

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Set your environment variables in a `.env` file (see below)
3. Start the server: `uvicorn app.app:app --reload`
4. POST YouTube video ID, upload transcript file, or paste transcript text to endpoints

### Tool Chat Endpoint

Interact with summarization tools by POSTing to `/tools` with a JSON body specifying the tool and its parameters. Example:

```json
{
	"tool": "summarize_transcript",
	"params": {
		"transcript": "Paste your transcript here.",
		"source": "teams",
		"length": "short",
		"style": "bullets"
	}
}
```

Available tools:

- `summarize_transcript`: Summarize any transcript (params: transcript, source, length, style)
- `summarize_youtube_video`: Summarize a YouTube video by URL (params: url)
- `summarize_teams_transcript`: Summarize a Teams transcript (params: transcript)

Example curl:

```sh
curl -X POST "http://localhost:8000/tools" \
	-H "Content-Type: application/json" \
	-d '{
		"tool": "summarize_transcript",
		"params": {"transcript": "Paste your transcript here.", "source": "teams", "length": "short", "style": "bullets"}
	}'
```

### Environment Variables
Create a `.env` file in the project root with:
```
MODEL_DEPLOYMENT_NAME=your-model-name
FOUNDRY_PROJECT_URL=https://your-foundry-endpoint.openai.azure.com/
FOUNDRY_API_KEY=your-api-key
```

## Foundry Integration
- Summarization is performed using a Microsoft Foundry agent (see `app/app.py`).
- Set your Foundry project endpoint and model deployment name in the `.env` file.


## How to Use with a Transcript File
- Simply copy or save your transcript as a plain text file (e.g., `transcript.txt`) into the `transcripts/` folder.
- Then, upload it using the file upload endpoint:

```sh
curl -X POST "http://localhost:8000/summarize/upload" -F "file=@transcripts/transcript.txt"
```

