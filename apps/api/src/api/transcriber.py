"""Access to the transcription service."""

from typing import Protocol

import httpx2

HEALTH_TIMEOUT_SECONDS = 2.0


class TranscriberClient(Protocol):
    """What the API needs from the transcription service."""

    async def is_healthy(self) -> bool:
        """Return whether the transcription service is reachable and healthy."""
        ...


class HttpTranscriberClient:
    """Talks to the transcription service over HTTP."""

    def __init__(
        self,
        base_url: str,
        timeout: float = HEALTH_TIMEOUT_SECONDS,
        transport: httpx2.AsyncBaseTransport | None = None,
    ) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self._transport = transport

    async def is_healthy(self) -> bool:
        try:
            async with httpx2.AsyncClient(
                base_url=self._base_url, timeout=self._timeout, transport=self._transport
            ) as client:
                response = await client.get("/health")
        except httpx2.HTTPError:
            return False
        return response.is_success
