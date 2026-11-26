"""HTTP entry point of the API."""

import os
from typing import Annotated

from fastapi import Depends, FastAPI

from api.transcriber import HttpTranscriberClient, TranscriberClient

DEFAULT_TRANSCRIBER_URL = "http://localhost:9000"

app = FastAPI(title="TranscriptDeck API")


def get_transcriber_client() -> TranscriberClient:
    """Build the transcriber client from the environment."""
    return HttpTranscriberClient(os.environ.get("TRANSCRIBER_URL", DEFAULT_TRANSCRIBER_URL))


@app.get("/api/health")
async def health(
    transcriber: Annotated[TranscriberClient, Depends(get_transcriber_client)],
) -> dict[str, str]:
    """Report the API status and whether the transcription service is reachable."""
    transcriber_status = "ok" if await transcriber.is_healthy() else "unreachable"
    return {"status": "ok", "transcriber": transcriber_status}
