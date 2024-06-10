from fastapi import Depends
from fastapi.testclient import TestClient

from src.api.dependencies import Session, get_db
from src.main import app
from src.schemas.task import CreateTask


def test_ping(test_client: TestClient) -> None:
  response = test_client.get("/ping")
  create_task = CreateTask(content="test content")

  payload = create_task.model_dump()

  response = test_client.post("/tasks/", json=payload)

  assert response.status_code == 201


def test_ping2(test_client: TestClient) -> None:
  response = test_client.get("/ping")
  assert response.status_code == 200
  assert response.json() == {
    "ping": "pong!",
    "environment": "dev",
    "testing": True,
  }
