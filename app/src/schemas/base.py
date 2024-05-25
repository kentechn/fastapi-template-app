from enum import Enum
from typing import Annotated, Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
  model_config = ConfigDict(alias_generator=to_camel)

  size: int
  page: int
  total_count: int
  data: list[T]


class SortOrderEnum(Enum):
  asc = "asc"
  desc = "desc"


class GetListQueryParams(BaseModel):
  size: Annotated[
    int,
    Query(description="取得するデータの最大取得数", ge=1, le=100, default=10),
  ]
  page: Annotated[
    int,
    Query(description="取得するタスクのページ数", ge=1, default=1),
  ]
  sort_order: Annotated[
    SortOrderEnum,
    Query(description="取得するタスクのソート順", default=SortOrderEnum.desc),
  ]
  """GETリクエストのクエリパラメータを表すクラス"""
