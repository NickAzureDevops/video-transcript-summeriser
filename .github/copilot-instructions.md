# Custom instructions for Copilot in this workspace

- This project summarizes YouTube videos via a GitHub Agentic Workflow (gh-aw),
  not a server or cloud service.
- The workflow lives in `.github/workflows/summarize-youtube.md`; edit that file,
  then run `gh aw compile` to regenerate `summarize-youtube.lock.yml`. Commit both.
- Never hand-edit the generated `.lock.yml`.
- `get_transcript.py` fetches a YouTube transcript as plain text; the Copilot
  agent writes the summary itself.
- Keep the project dependency-light: no Azure/Foundry, no API keys.
- Update README.md as behavior changes.
