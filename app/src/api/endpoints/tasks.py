from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import Session, get_db
from src.cruds import crud_tasks
from src.schemas.task import (
  CreateTask,
  GetTodoListQueryParams,
  TaskInDB,
  TaskResponse,
  TasksResponse,
  UpdateTask,
)

router = APIRouter()


@router.get("/", response_model=TasksResponse, response_model_exclude_unset=True)
def read_tasks(
  query_params: GetTodoListQueryParams = Depends(), db: Session = Depends(get_db)
) -> TasksResponse:
  """
  プロバイダされたクエリパラメータに基づいて、タスクのリストを取得します。

  Args:
  - query_params: タスクをフィルタリングするためのクエリパラメータを含むGetTodoListQueryParamsのインスタンスです。
  - db: データベースセッションのインスタンスです。

  returns:
  - データベースから取得したタスクのリストを含むTasksResponseオブジェクトです。
  """
  print(query_params)

  data, total_count = crud_tasks.get_db_obj_list(db, query_params)

  tasks = [TaskResponse(**item.__dict__) for item in data]

  res_data = TasksResponse(
    limit=query_params.limit,
    offset=query_params.offset,
    totalCount=total_count,
    data=tasks,
  )

  return res_data


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
  """
  指定されたタスクIDに基づいてデータベースからタスクを取得します。

  Parameters:
    task_id (int): 取得するタスクのID
    db (Session, optional): データベースセッション (デフォルトはget_db関数によって提供される)

  Returns:
    TaskResponse: タスクのレスポンスモデル
  """
  task = crud_tasks.get_db_obj_by_id(db, task_id)

  if task is None:
    raise HTTPException(
      status_code=404,
      detail="タスクが見つかりませんでした。",
    )

  return TaskResponse(id=task.id, isCompleted=task.is_completed, content=task.content)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: CreateTask, db: Session = Depends(get_db)) -> TaskResponse:
  """
  新しいタスクをデータベースに作成します。

  Args:
    task (CreateTask): 作成するタスクの情報が含まれるオブジェクト
    db (Session): データベースセッション

  Returns:
    TaskResponse: 作成されたタスクの情報が含まれるオブジェクト
  """
  # Logic to create a new task in the database
  return crud_tasks.create_db_obj(db, task)


@router.put("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task(task_id: int, task: UpdateTask, db: Session = Depends(get_db)) -> None:
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
  target_task = crud_tasks.get_db_obj_by_id(db, task_id)

  if target_task is None:
    raise HTTPException(
      status_code=404,
      detail="タスクが見つかりませんでした。",
    )

  crud_tasks.update_db_obj(db, target_task, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def real_delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
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
  target_task = crud_tasks.get_db_obj_by_id(db, task_id)

  if target_task is None:
    raise HTTPException(
      status_code=404,
      detail="タスクが見つかりませんでした。",
    )

  crud_tasks.real_delete_db_obj(db, target_task)
