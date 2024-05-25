from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_read_tasks() -> None:
  response = client.get("/tasks")
  assert response.status_code == 200
