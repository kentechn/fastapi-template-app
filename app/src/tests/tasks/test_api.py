from fastapi.testclient import TestClient

# from src.api.dependencies import Session
from src.models.task import Task
from src.schemas.task import TaskResponse


def test_get_tasks_api(test_client: TestClient, insert_tasks: list[Task]) -> None:
  response = test_client.get("/tasks/")

  tasks = [
    TaskResponse(
      id=task.id, content=task.content, isCompleted=task.is_completed
    ).model_dump(by_alias=True)
    for task in insert_tasks
  ]

  print("tasks:")
  print(tasks)

  assert response.status_code == 200
  assert response.json() == {"limit": 10, "offset": 0, "data": tasks, "totalCount": 3}
