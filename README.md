# video-transcript-summeriser

Summarize a YouTube video by opening a GitHub issue with its link. A
[GitHub Agentic Workflow](https://github.github.com/gh-aw/) fetches the video's
transcript and posts a concise summary back as a comment — powered by GitHub
Copilot, with no external API keys or cloud services.

## How it works

1. You open (or reopen) an issue containing a YouTube URL in its body.
2. The workflow [.github/workflows/summarize-youtube.md](.github/workflows/summarize-youtube.md):
   - installs dependencies and runs [get_transcript.py](get_transcript.py) to
     fetch the captions,
   - asks the Copilot agent to summarize the transcript,
   - posts the summary as a comment on the issue.

The agent itself writes the summary, so there is no model deployment or API key
to manage.

## Files

| File | Purpose |
|------|---------|
| [.github/workflows/summarize-youtube.md](.github/workflows/summarize-youtube.md) | Workflow source (edit this) |
| `.github/workflows/summarize-youtube.lock.yml` | Compiled workflow that GitHub Actions runs (generated — do not edit by hand) |
| [get_transcript.py](get_transcript.py) | Fetches a YouTube transcript as plain text |
| [requirements.txt](requirements.txt) | Just `youtube-transcript-api` |

After editing the `.md`, run `gh aw compile` to regenerate the `.lock.yml`, then
commit both.

## Local use

Fetch a transcript directly:

```sh
pip install -r requirements.txt
python3 get_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Requirements

- The [`gh aw`](https://github.com/githubnext/gh-aw) CLI extension to edit and
  compile the workflow.
- GitHub Copilot enabled for the repository (the workflow's engine).

## Caveat

YouTube sometimes blocks transcript requests from cloud/datacenter IPs, so the
workflow can be intermittent on GitHub-hosted runners. If that happens, run it on
a self-hosted runner or via a proxy. It works reliably locally.
