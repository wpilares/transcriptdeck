import asyncio

import httpx2

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
