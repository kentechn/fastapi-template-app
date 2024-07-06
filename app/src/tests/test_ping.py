from fastapi.testclient import TestClient

from src.schemas.task import CreateTask


def test_ping(test_client: TestClient) -> None:
  create_task = CreateTask(content="test content")

  payload = create_task.model_dump()

  response = test_client.post("/tasks/", json=payload)

  assert response.status_code == 201
