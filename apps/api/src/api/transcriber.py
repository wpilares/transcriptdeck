"""Access to the transcription service."""

import asyncio
from typing import Protocol

import httpx2

# Upper bound for the whole health check, not for each phase of the HTTP request.
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
        # A health probe must never fail its caller: a malformed URL (httpx2.InvalidURL is
        # not an httpx2.HTTPError), a network error and an overrun all mean "not healthy".
        try:
            # The client timeout applies to each phase (connect, read, write, pool), so a
            # slow service could outlast it several times over; this bounds the total.
            async with (
                asyncio.timeout(self._timeout),
                httpx2.AsyncClient(
                    base_url=self._base_url, timeout=self._timeout, transport=self._transport
                ) as client,
            ):
                response = await client.get("/health")
        except Exception:
            return False
        return response.is_success
