from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from src.api.dependencies import Session
from src.models.task import Task
from src.schemas.task import (
  CreateTask,
  GetTodoListQueryParams,
  TaskResponse,
  TasksResponse,
  UpdateTask,
)


def get_db_obj_list(db: Session, query_params: GetTodoListQueryParams) -> TasksResponse:
  """
  データベースからタスクのリストを取得します。

  Parameters:
    db (Session): データベースセッション

  Returns:
    TasksResponse: タスクのリストを含むレスポンスオブジェクト
  """
  stmt = select(Task)
  if query_params.is_completed is not None:
    stmt = stmt.where(Task.is_completed == query_params.is_completed)

  if query_params.sort_field is not None:
    sort_field = query_params.sort_field
    sort_order = query_params.sort_order

    if sort_field == "content":
      if sort_order == "asc":
        stmt = stmt.order_by(Task.content.asc())
      else:
        stmt = stmt.order_by(Task.content.desc())

    elif sort_field == "created_at":
      if sort_order == "asc":
        stmt = stmt.order_by(Task.created_at.asc())
      else:
        stmt = stmt.order_by(Task.created_at.desc())

    elif sort_field == "updated_at":
      if sort_order == "asc":
        stmt = stmt.order_by(Task.updated_at.asc())
      else:
        stmt = stmt.order_by(Task.updated_at.desc())

    elif sort_field == "is_completed":
      if sort_order == "asc":
        stmt = stmt.order_by(Task.is_completed.asc())
      else:
        stmt = stmt.order_by(Task.is_completed.desc())

    size = query_params.size
    page = query_params.page

    stmt = stmt.limit(size).offset((page - 1) * size)

    # Add more conditions for other fields if needed
  tasks = db.execute(stmt).scalars().all()

  data = [
    TaskResponse(id=task.id, isCompleted=task.is_completed, content=task.content)
    for task in tasks
  ]

  res_data = TasksResponse(page=1, size=2, totalCount=2, data=data)

  return res_data


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
