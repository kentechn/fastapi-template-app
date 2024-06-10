from sqlalchemy.orm import Session

from src.models.task import Task
from src.repositories.base import BaseRepository
from src.schemas.task import CreateTask, GetTasksQueryParams, UpdateTask


class TaskRepository(BaseRepository[Task, CreateTask, UpdateTask]):
  def __init__(self) -> None:
    super().__init__(Task)

  def get_tasks_list(self, db: Session, query: GetTasksQueryParams) -> list[Task]:
    return self.get_db_obj_list(db)

  def create_task(self, db: Session, task: CreateTask) -> Task:
    return self.create(db, task)

  def get_task_by_id(self, db: Session, task_id: int) -> Task | None:
    return self.get_db_obj_by_id(db, task_id)

  def update_task(
    self, db: Session, task_id: int, update_task: UpdateTask
  ) -> Task | None:
    task = self.get_db_obj_by_id(db, task_id)

    return self.update(db, task, update_task)

  def delete_task(self, db: Session, task_id: int) -> Task | None:
    task = self.get_db_obj_by_id(db, task_id)
    return self.real_delete(db, task)
