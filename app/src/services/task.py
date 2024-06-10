from sqlalchemy.orm import Session

from src.models.task import Task
from src.repositories.task import TaskRepository
from src.schemas.task import GetTasksQueryParams, TaskResponse, TasksResponse


class TaskService:
  def __init__(self) -> None:
    self.task_repo = TaskRepository()

  def get_tasks_list(self, db: Session, query: GetTasksQueryParams) -> TasksResponse:
    result, total_count = self.task_repo.get_tasks_list(db)
    tasks = [TaskResponse(**item.__dict__) for item in result]

    res_data = TasksResponse(
      limit=query.limit,
      offset=query.offset,
      totalCount=total_count,
      data=tasks,
    )

    return
