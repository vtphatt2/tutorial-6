import pytest
from fastapi.testclient import TestClient
from src.api.auth import create_demo_token
from src.main import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


@pytest.fixture
def manager_headers() -> dict[str, str]:
    return {"Authorization": "Bearer " + create_demo_token("manager@fieldco.com", "manager")}


@pytest.fixture
def technician_headers() -> dict[str, str]:
    return {"Authorization": "Bearer " + create_demo_token("alex@fieldco.com", "technician")}
