from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_missing_token_is_rejected(client: TestClient) -> None:
    assert client.get("/demo/jobs").status_code == 401


def test_manager_can_view_seed_data(client: TestClient, manager_headers: dict[str, str]) -> None:
    jobs = client.get("/demo/jobs", headers=manager_headers)
    assert jobs.status_code == 200
    assert len(jobs.json()) == 2
    techs = client.get("/demo/technicians", headers=manager_headers)
    assert techs.status_code == 200
    assert len(techs.json()) == 2


def test_technician_cannot_view_all_jobs(client: TestClient, technician_headers: dict[str, str]) -> None:
    assert client.get("/demo/jobs", headers=technician_headers).json() == []
    assert client.get("/demo/technicians", headers=technician_headers).status_code == 403
