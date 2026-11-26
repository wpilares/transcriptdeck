"""HTTP entry point of the transcription service."""

from fastapi import FastAPI

app = FastAPI(title="TranscriptDeck Transcriber")


@app.get("/health")
async def health() -> dict[str, str]:
    """Report that the service is up."""
    return {"status": "ok"}
