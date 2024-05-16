from typing import Annotated

from fastapi import APIRouter, Query, status

from src.schemas.task import (
  CreateTask,
  TaskResponse,
  TasksResponse,
  UpdateTask,
)

router = APIRouter()


@router.get("/", response_model=TasksResponse, response_model_exclude_unset=True)
def read_tasks(q: Annotated[str | None, Query(max_length=50)] = None) -> TasksResponse:
  # Logic to fetch all tasks from the database using query_params
  pass


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int) -> TaskResponse:
  # Logic to fetch a specific task by task_id from the database
  pass


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: CreateTask) -> TaskResponse:
  # Logic to create a new task in the database
  pass


@router.put("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task(task_id: int, task: UpdateTask) -> None:
  # Logic to update a specific task by task_id in the database
  pass


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
  # Logic to delete a specific task by task_id from the database
  pass
