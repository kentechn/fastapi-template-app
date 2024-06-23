from sqlalchemy.orm import Session

# from src.models.task import Task
from src.repositories.task import TaskRepository, task_repo
from src.schemas.base import PagingQueryIn
from src.schemas.task import (
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


task_service = TaskService(task_repo)
