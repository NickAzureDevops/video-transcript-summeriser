
# Minimal, focused tools for MCP demo
async def summarize_transcript(transcript: str, source: str = "generic", length: str = "medium", style: str = "paragraph") -> str:
    summary = transcript[:300]
    return f"[LOCAL TEST SUMMARY]\n{'-'*40}\n{summary}\n{'-'*40}\n(End of preview)"

def search_transcript(transcript: str, query: str) -> str:
    lines = transcript.splitlines()
    matches = [f"Line {i+1}: {line.strip()}" for i, line in enumerate(lines) if query.lower() in line.lower()]
    if matches:
        return f"Search results for '{query}':\n" + "\n".join(matches)
    return f"No matches found for '{query}'."

def search_transcript(transcript: str, query: str) -> str:
    """Return all lines from the transcript containing the query (case-insensitive)."""
    lines = transcript.splitlines()
    matches = [line for line in lines if query.lower() in line.lower()]
    if matches:
        return '\n'.join(matches)
    return f"No matches found for '{query}'."