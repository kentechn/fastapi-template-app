from fastapi import APIRouter, Depends, status

from src.api.dependencies import Session, get_db
from src.schemas.base import PagingQueryIn
from src.schemas.task import (
  CreateTask,
  TaskResponse,
  TasksQueryParams,
  TasksResponse,
  TasksSortQueryIn,
  UpdateTask,
)
from src.services.task import TaskService, task_service

router = APIRouter()


# Dependency Injection
def get_task_service() -> TaskService:
  return task_service


@router.get("/", response_model=TasksResponse, response_model_exclude_unset=True)
def read_tasks(
  page_params: PagingQueryIn = Depends(),
  sort_params: TasksSortQueryIn = Depends(),
  query_params: TasksQueryParams = Depends(),
  db: Session = Depends(get_db),
  service: TaskService = Depends(get_task_service),
) -> TasksResponse:
  """
  プロバイダされたクエリパラメータに基づいて、タスクのリストを取得します。

  Args:
  - query_params: タスクをフィルタリングするためのクエリパラメータを含むGetTodoListQueryParamsのインスタンスです。
  - db: データベースセッションのインスタンスです。

  returns:
  - データベースから取得したタスクのリストを含むTasksResponseオブジェクトです。
  """
  return service.get_tasks_list(db, page_params, sort_params, query_params)


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
  task_id: int,
  db: Session = Depends(get_db),
  service: TaskService = Depends(get_task_service),
) -> TaskResponse:
  """
  指定されたタスクIDに基づいてデータベースからタスクを取得します。

  Parameters:
    task_id (int): 取得するタスクのID
    db (Session, optional): データベースセッション (デフォルトはget_db関数によって提供される)

  Returns:
    TaskResponse: タスクのレスポンスモデル
  """
  return service.get_task(db, task_id)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
  task: CreateTask,
  db: Session = Depends(get_db),
  service: TaskService = Depends(get_task_service),
) -> TaskResponse:
  """
  新しいタスクをデータベースに作成します。

  Args:
    task (CreateTask): 作成するタスクの情報が含まれるオブジェクト
    db (Session): データベースセッション

  Returns:
    TaskResponse: 作成されたタスクの情報が含まれるオブジェクト
  """
  # Logic to create a new task in the database
  return service.create_task(db, task)


@router.put("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task(
  task_id: int,
  task: UpdateTask,
  db: Session = Depends(get_db),
  service: TaskService = Depends(get_task_service),
) -> None:
  """
  プロバイダされたタスクIDに基づいて、タスクを更新します。

  Args:
  - task_id: 更新するタスクのIDです。
  - task: 更新するタスクの情報を含むUpdateTaskオブジェクトです。
  - db: データベースセッションのインスタンスです。

  Returns:
  - None: タスクの更新が成功した場合、何も返しません。

  Raises:
  - HTTPException(404): 指定されたタスクIDが見つからない場合に発生します。
  """

  service.update_task(db, task_id, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def real_delete_task(
  task_id: int,
  db: Session = Depends(get_db),
  service: TaskService = Depends(get_task_service),
) -> None:
  """
  指定されたタスクをデータベースから完全に削除します。

  Args:
    task_id (int): 削除するタスクのID
    db (Session): データベースセッション

  Raises:
    HTTPException: タスクが見つからない場合に発生します。

  Returns:
    None
  """
  service.delete_task(db, task_id)
