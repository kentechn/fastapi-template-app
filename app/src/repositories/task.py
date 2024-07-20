from sqlalchemy.orm import Session

from src.models.task import Task
from src.repositories.base import BaseRepository
from src.schemas.base import PagingQueryIn
from src.schemas.task import (
  CreateTask,
  TasksQueryParams,
  TasksSortQueryIn,
  UpdateTask,
)


class TaskRepository(
  BaseRepository[Task, CreateTask, UpdateTask, TasksQueryParams, TasksSortQueryIn]
):
  def __init__(self) -> None:
    super().__init__(Task)

  def get_tasks_list(
    self,
    db: Session,
    page_params: PagingQueryIn,
    sort_params: TasksSortQueryIn,
    query_params: TasksQueryParams,
  ) -> tuple[list[Task], int]:
    return self.get_db_obj_list(db, page_params, sort_params, query_params)

  def get_task_by_id(self, db: Session, task_id: int) -> Task | None:
    return self.get_db_obj_by_id(db, task_id)

  def create_task(self, db: Session, task: CreateTask) -> Task:
    return self.create(db, task)

  def update_task(
    self, db: Session, task_id: int, update_task: UpdateTask
  ) -> Task | None:
    task = self.get_db_obj_by_id(db, task_id)

    if task is None:
      return None

    return self.update(db, task, update_task)

  def delete_task(self, db: Session, task_id: int) -> Task | None:
    task = self.get_db_obj_by_id(db, task_id)

    if task is None:
      return None

    return self.real_delete(db, task)


task_repo = TaskRepository()
