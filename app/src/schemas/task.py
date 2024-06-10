from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import Query
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.schemas.base import GetListQueryParams, ListResponse


class BaseTask(BaseModel):
  content: str
  """ベースタスクを表すクラス"""


class TaskInDB(BaseTask):
  id: int
  is_completed: bool
  created_at: datetime
  updated_at: datetime
  """データベース内のタスクを表すクラス"""

  model_config = ConfigDict(from_attributes=True)


class CreateTask(BaseTask):
  model_config = ConfigDict(alias_generator=to_camel)

  is_completed: bool = False
  """タスクの作成情報を表すクラス"""


class UpdateTask(BaseTask):
  model_config = ConfigDict(alias_generator=to_camel)

  is_completed: bool
  """タスクの更新情報を表すクラス"""


class DeleteTasks(BaseModel):
  ids: list[int]
  """タスクの一括削除リクエストボディを表すクラス"""


class TaskResponse(BaseTask):
  model_config = ConfigDict(alias_generator=to_camel)

  id: int
  is_completed: bool = Field(
    validation_alias=AliasChoices("is_completed", "isCompleted")
  )
  """タスクのレスポンス情報を表すクラス"""


class TasksResponse(ListResponse[TaskResponse]):
  pass
  """タスクのリストレスポンス情報を表すクラス"""


class TodoSortFieldEnum(Enum):
  created_at = "created_at"
  content = "content"


class GetTasksQueryParams(GetListQueryParams):
  model_config = ConfigDict(alias_generator=to_camel)

  sort_field: Annotated[TodoSortFieldEnum, Query(default=TodoSortFieldEnum.created_at)]
  content: Annotated[str | None, Query(max_length=50, default=None)]
  is_completed: Annotated[bool, Query(default=False)]
  # created_at: Annotated[str | None, Query] = None
  # updated_at: Annotated[str | None, Query] = None
  """GETリクエストのクエリパラメータを表すクラス"""
