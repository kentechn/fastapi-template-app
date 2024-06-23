from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select

from src.api.dependencies import Session
from src.models.task import Task
from src.schemas.base import PagingQueryIn
from src.schemas.task import (
  CreateTask,
  TaskResponse,
  TasksQueryParams,
  TasksSortQueryIn,
  UpdateTask,
)


def get_db_obj_list(
  db: Session,
  page_params: PagingQueryIn,
  sort_params: TasksSortQueryIn,
  query_params: TasksQueryParams,
) -> tuple[list[Task], int]:
  """
  データベースからタスクのリストを取得します。

  Parameters:
    db (Session): データベースセッション

  Returns:
    TasksResponse: タスクのリストを含むレスポンスオブジェクト
  """
  stmt = select(Task)
  stmt = query_params.apply_to_query(stmt)

  # Get total count
  total_count_stmt = select(func.count()).select_from(stmt.subquery())
  total_count = db.execute(total_count_stmt).scalar()

  # Apply sorting
  stmt = sort_params.apply_to_query(stmt)

  # Apply paging
  stmt = page_params.apply_to_query(stmt)

  # Add more conditions for other fields if needed
  tasks = db.execute(stmt).scalars().all()

  return tasks, total_count


def get_db_obj_by_id(db: Session, id: int) -> Task | None:
  """
  指定されたIDに基づいてデータベースからタスクオブジェクトを取得します。

  Parameters:
    - db (Session): データベースセッションオブジェクト
    - id (int): タスクのID

  Returns:
    - Task | None: タスクオブジェクトまたはNone
  """
  stmt = select(Task).where(Task.id == id)
  task = db.execute(stmt).scalars().one_or_none()

  return task


def create_db_obj(db: Session, task_create: CreateTask) -> TaskResponse:
  """
  データベースに新しいタスクを作成します。

  Args:
    db (Session): データベースセッション。
    task_create (CreateTask): 作成するタスクデータ。

  Returns:
    TaskResponse: 作成されたタスクデータを含むレスポンス。

  """
  create_dict = jsonable_encoder(task_create, by_alias=False)
  db_obj = Task(**create_dict)
  db.add(db_obj)
  db.flush()
  db.refresh(db_obj)

  res_data = TaskResponse(
    id=db_obj.id, isCompleted=db_obj.is_completed, content=db_obj.content
  )

  return res_data


def update_db_obj(db: Session, db_obj: Task, task_update: UpdateTask) -> TaskResponse:
  """
  データベース内のタスクを更新します。

  Args:
    db (Session): データベースセッション。
    task_update (UpdateTask): 更新されたタスクデータ。

  Returns:
    TaskResponse: 更新されたタスクデータを含むレスポンス。
  """
  # task_updateオブジェクトを辞書に変換し、未設定の値を除外する
  update_dict = jsonable_encoder(task_update, by_alias=False, exclude_unset=True)

  for field in update_dict:
    setattr(db_obj, field, update_dict[field])

  db.add(db_obj)
  db.flush()
  db.refresh(db_obj)

  res_data = TaskResponse(
    id=db_obj.id, isCompleted=db_obj.is_completed, content=db_obj.content
  )

  return res_data


def real_delete_db_obj(db: Session, db_obj: Task) -> None:
  """
  データベースからタスクを削除します。

  Args:
    db (Session): データベースセッション。
    db_obj (Task): 削除するタスクオブジェクト。

  Returns:
    None
  """
  db.delete(db_obj)
  db.flush()
