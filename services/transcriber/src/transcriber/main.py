from fastapi import FastAPI

app = FastAPI(title="TranscriptDeck Transcriber")


@app.get("/health", description="Report that the service is up.")
async def health() -> dict[str, str]:
    return {"status": "ok"}
