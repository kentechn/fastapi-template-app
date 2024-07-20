from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import Query
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from sqlalchemy import Select

from src.models.task import Task
from src.schemas.base import ListResponse, ModelQueryParams, SortQueryIn


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


class TasksSortFieldEnum(Enum):
  created_at = "created_at"
  updated_at = "updated_at"
  content = "content"
  is_completed = "is_completed"


class TasksSortQueryIn(SortQueryIn):
  sort_by: Annotated[TasksSortFieldEnum, Query(default=TasksSortFieldEnum.created_at)]


class TasksQueryParams(ModelQueryParams):
  content: Annotated[str | None, Query(max_length=50, default=None)]
  is_completed: Annotated[bool | None, Query(default=None)]
  # created_at: Annotated[str | None, Query] = None
  # updated_at: Annotated[str | None, Query] = None

  def apply_to_query(self, query: Select) -> Select:
    if self.content is not None:
      query = query.filter(Task.content.like(f"%{self.content}%"))
    if self.is_completed is not None:
      query = query.filter(Task.is_completed == self.is_completed)
    # if self.created_at is not None:
    #   query = query.filter(Task.created_at == self.created_at)
    # if self.updated_at is not None:
    #   query = query.filter(Task.updated_at == self.updated_at)
    return query

  """GETリクエストのクエリパラメータを表すクラス"""
