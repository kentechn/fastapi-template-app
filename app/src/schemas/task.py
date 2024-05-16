from fastapi import Query
from pydantic import BaseModel

from src.schemas.base import GetListQueryParams, ListResponse


class BaseTask(BaseModel):
  content: str
  """ベースタスクを表すクラス"""


class TaskInDB(BaseTask):
  id: int
  is_completed: bool
  """データベース内のタスクを表すクラス"""


class CreateTask(BaseTask):
  is_completed: bool = False
  """タスクの作成情報を表すクラス"""


class UpdateTask(BaseTask):
  is_completed: bool
  """タスクの更新情報を表すクラス"""


class DeleteTasks(BaseModel):
  ids: list[int]
  """タスクの一括削除リクエストボディを表すクラス"""


class TaskResponse(BaseTask):
  id: int
  is_completed: bool
  """タスクのレスポンス情報を表すクラス"""


class TasksResponse(ListResponse[TaskResponse]):
  pass
  """タスクのリストレスポンス情報を表すクラス"""


class TaskQueryParams(GetListQueryParams):
  pass
  """GETリクエストのクエリパラメータを表すクラス"""


# TaskResponseをインスタンス化してデータを追加
# task_response = TaskResponse(
#   limit=10,
#   offset=0,
#   total_count=2,
#   data=[
#     Task(task_id=1, content="Task 1", is_completed=False),
#     Task(task_id=2, content="Task 2", is_completed=True),
#   ],
# )
