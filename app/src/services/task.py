from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.task import Task
from src.repositories.task import TaskRepository, task_repo
from src.schemas.base import PagingQueryIn
from src.schemas.task import (
  CreateTask,
  TaskResponse,
  TasksQueryParams,
  TasksResponse,
  TasksSortQueryIn,
  UpdateTask,
)


class TaskService:
  def __init__(self, repo: TaskRepository) -> None:
    self.task_repo = repo

  def get_tasks_list(
    self,
    db: Session,
    page_params: PagingQueryIn,
    sort_params: TasksSortQueryIn,
    query_params: TasksQueryParams,
  ) -> TasksResponse:
    result, total_count = self.task_repo.get_tasks_list(
      db, page_params, sort_params, query_params
    )
    tasks = [TaskResponse(**item.__dict__) for item in result]

    res_data = TasksResponse(
      size=page_params.size,
      page=page_params.page,
      totalCount=total_count,
      data=tasks,
    )

    return res_data

  def get_task(self, db: Session, task_id: int) -> TaskResponse:
    result = self.task_repo.get_task_by_id(db, task_id)

    if result is None:
      raise HTTPException(
        status_code=404,
        detail="タスクが見つかりませんでした。",
      )

    return TaskResponse(**result.__dict__)

  def create_task(self, db: Session, create_task: CreateTask) -> TaskResponse:
    result = self.task_repo.create_task(db, create_task)
    return TaskResponse(**result.__dict__)

  def update_task(self, db: Session, task_id: int, update_task: UpdateTask) -> Task:
    result = self.task_repo.update_task(db, task_id, update_task)

    if result is None:
      raise HTTPException(
        status_code=404,
        detail="タスクが見つかりませんでした。",
      )

    return result

  def delete_task(self, db: Session, task_id: int) -> Task:
    result = self.task_repo.delete_task(db, task_id)

    if result is None:
      raise HTTPException(
        status_code=404,
        detail="タスクが見つかりませんでした。",
      )

    return result


task_service = TaskService(task_repo)
