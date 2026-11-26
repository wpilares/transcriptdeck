from fastapi.testclient import TestClient

from api.main import app, get_transcriber_client


class FakeTranscriberClient:
    def __init__(self, healthy: bool) -> None:
        self._healthy = healthy

    async def is_healthy(self) -> bool:
        return self._healthy


def get_health(healthy: bool):
    app.dependency_overrides[get_transcriber_client] = lambda: FakeTranscriberClient(healthy)
    try:
        return TestClient(app).get("/api/health")
    finally:
        app.dependency_overrides.clear()


def test_health_reports_transcriber_ok_when_reachable() -> None:
    response = get_health(healthy=True)

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "transcriber": "ok"}


def test_health_still_answers_when_transcriber_is_unreachable() -> None:
    response = get_health(healthy=False)

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "transcriber": "unreachable"}
