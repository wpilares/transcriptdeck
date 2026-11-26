import asyncio
import time

import httpx2
import pytest

from api.transcriber import HttpTranscriberClient


def is_healthy(handler) -> bool:
    client = HttpTranscriberClient(
        "http://transcriber.test", transport=httpx2.MockTransport(handler)
    )
    return asyncio.run(client.is_healthy())


def test_is_healthy_when_transcriber_answers_ok() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url == "http://transcriber.test/health"
        return httpx2.Response(200, json={"status": "ok"})

    assert is_healthy(handler) is True


def test_is_not_healthy_when_transcriber_answers_with_an_error() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(503)

    assert is_healthy(handler) is False


def test_is_not_healthy_when_connection_fails() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.ConnectError("connection refused", request=request)

    assert is_healthy(handler) is False


@pytest.mark.parametrize("base_url", ["http://host:abc", "http://[::1"])
def test_is_not_healthy_when_the_url_is_malformed(base_url: str) -> None:
    client = HttpTranscriberClient(base_url)

    assert asyncio.run(client.is_healthy()) is False


def test_is_not_healthy_when_the_check_exceeds_the_total_time_bound() -> None:
    async def handler(request: httpx2.Request) -> httpx2.Response:
        await asyncio.sleep(1)
        return httpx2.Response(200, json={"status": "ok"})

    client = HttpTranscriberClient(
        "http://transcriber.test", timeout=0.05, transport=httpx2.MockTransport(handler)
    )

    started = time.monotonic()
    healthy = asyncio.run(client.is_healthy())
    elapsed = time.monotonic() - started

    assert healthy is False
    assert elapsed < 0.5
