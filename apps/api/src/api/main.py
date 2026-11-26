import os
from typing import Annotated

from fastapi import Depends, FastAPI

from api.transcriber import HttpTranscriberClient, TranscriberClient

DEFAULT_TRANSCRIBER_URL = "http://localhost:9000"

app = FastAPI(title="TranscriptDeck API")


def get_transcriber_client() -> TranscriberClient:
    return HttpTranscriberClient(os.environ.get("TRANSCRIBER_URL", DEFAULT_TRANSCRIBER_URL))


@app.get(
    "/api/health",
    description="Report the API status and whether the transcription service is reachable.",
)
async def health(
    transcriber: Annotated[TranscriberClient, Depends(get_transcriber_client)],
) -> dict[str, str]:
    transcriber_status = "ok" if await transcriber.is_healthy() else "unreachable"
    return {"status": "ok", "transcriber": transcriber_status}
