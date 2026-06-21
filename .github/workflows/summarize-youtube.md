---
description: |
  Summarizes a YouTube video linked in a GitHub issue. When an issue is opened
  or reopened with a YouTube URL in its body, this workflow fetches the video's
  transcript and posts a concise summary back as a comment.

on:
  issues:
    types: [opened, reopened]
  reaction: eyes

permissions:
  contents: read
  issues: read

network: defaults

engine: copilot

steps:
  - name: Set up Python
    uses: actions/setup-python@v5
    with:
      python-version: "3.13"
  - name: Install dependencies
    run: pip install -r requirements.txt
  - name: Fetch transcript
    env:
      ISSUE_BODY: ${{ github.event.issue.body }}
    run: |
      if ! printf '%s' "$ISSUE_BODY" | grep -qiE 'youtube\.com|youtu\.be'; then
        echo "NO_URL_FOUND" > transcript.txt
      elif ! python3 get_transcript.py "$ISSUE_BODY" > transcript.txt 2> fetch_error.txt; then
        printf 'FETCH_FAILED: %s' "$(cat fetch_error.txt)" > transcript.txt
      fi

tools:
  bash: true

safe-outputs:
  add-comment:

timeout-minutes: 10
---

# Summarize or translate a YouTube video

A new issue (#${{ github.event.issue.number }}) was opened. A setup step has
already fetched the video transcript (translated to English when necessary) into
the file `transcript.txt` in the working directory.

Do the following:

1. Read the file `transcript.txt`.
2. If its contents are exactly `NO_URL_FOUND`, post a comment politely asking the
   issue author to include a YouTube link in the issue body, then stop.
3. If its contents start with `FETCH_FAILED:`, post a comment explaining that the
   transcript could not be retrieved (the video may have no captions, or YouTube
   blocked the request from the runner). Include the error detail that follows
   `FETCH_FAILED:`. Then stop.
4. Read the issue body (`${{ github.event.issue.body }}`). If it contains the
   word "translate" (case-insensitive), the user wants a **translation**:
   - Post the full translated transcript content as a comment, formatted in
     clear readable Markdown paragraphs. Do not condense or omit content.
   - Begin the comment with a short note indicating the language the video was
     translated from (if identifiable from the transcript).
5. Otherwise, **summarize** the transcript: write a 2-3 sentence overview, then
   4-6 bullet points of the key takeaways.

Post your result as a comment on the issue using the add-comment safe output.
Format it in clear Markdown. Do not invent content that is not supported by the
transcript.
