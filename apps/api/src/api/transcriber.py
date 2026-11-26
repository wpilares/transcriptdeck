import asyncio
from typing import Protocol

import httpx2

HEALTH_CHECK_TOTAL_TIMEOUT_SECONDS = 2.0


class TranscriberClient(Protocol):
    async def is_healthy(self) -> bool: ...


class HttpTranscriberClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = HEALTH_CHECK_TOTAL_TIMEOUT_SECONDS,
        transport: httpx2.AsyncBaseTransport | None = None,
    ) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self._transport = transport

    async def is_healthy(self) -> bool:
        try:
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
