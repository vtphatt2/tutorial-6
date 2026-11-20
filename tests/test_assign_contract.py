"""ACTIVITY 3: Tests intentionally RED until you implement the feature.

Run `uv run pytest tests/test_starter.py -q` before Activity 3 (should PASS).
Run `uv run pytest tests/test_assign_contract.py -q` after implementation.
"""
from uuid import UUID
from fastapi.testclient import TestClient
from src.repository.seed_store import JOB_A, TECH_A

URL = f"/jobs/{JOB_A}/assign"


def test_success(client: TestClient, manager_headers: dict[str, str]) -> None:
    r = client.post(URL, headers=manager_headers, json={"assignee_email": "alex@fieldco.com"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert UUID(body["job_id"]) == JOB_A
    assert body["assignee_email"] == "alex@fieldco.com"
    assert body["status"] == "assigned"
    jobs = client.get("/demo/jobs", headers=manager_headers).json()
    changed = next(j for j in jobs if j["id"] == str(JOB_A))
    assert changed["assignee_id"] == str(TECH_A)
    assert changed["status"] == "assigned"


def test_unavailable_technician(client: TestClient, manager_headers: dict[str, str]) -> None:
    r = client.post(URL, headers=manager_headers, json={"assignee_email": "sam@fieldco.com"})
    assert r.status_code == 409, r.text


def test_unknown_technician(client: TestClient, manager_headers: dict[str, str]) -> None:
    r = client.post(URL, headers=manager_headers, json={"assignee_email": "missing@fieldco.com"})
    assert r.status_code == 409, r.text


def test_unknown_job(client: TestClient, manager_headers: dict[str, str]) -> None:
    r = client.post('/jobs/00000000-0000-0000-0000-000000009999/assign',
                    headers=manager_headers, json={"assignee_email": "alex@fieldco.com"})
    assert r.status_code == 404, r.text


def test_role_is_forbidden(client: TestClient, technician_headers: dict[str, str]) -> None:
    r = client.post(URL, headers=technician_headers, json={"assignee_email": "alex@fieldco.com"})
    assert r.status_code == 403, r.text


def test_missing_token(client: TestClient) -> None:
    assert client.post(URL, json={"assignee_email": "alex@fieldco.com"}).status_code == 401


def test_missing_request_field_is_400(client: TestClient, manager_headers: dict[str, str]) -> None:
    r = client.post(URL, headers=manager_headers, json={})
    assert r.status_code == 400, r.text


def test_malformed_json_is_400(client: TestClient, manager_headers: dict[str, str]) -> None:
    r = client.post(URL, headers={**manager_headers, "Content-Type": "application/json"},
                    content='{broken')
    assert r.status_code == 400, r.text


def test_failed_assignment_does_not_change_data(client: TestClient, manager_headers: dict[str, str]) -> None:
    client.post(URL, headers=manager_headers, json={"assignee_email": "sam@fieldco.com"})
    jobs = client.get("/demo/jobs", headers=manager_headers).json()
    unchanged = next(j for j in jobs if j["id"] == str(JOB_A))
    assert unchanged["status"] == "unassigned"
    assert unchanged["assignee_id"] is None
