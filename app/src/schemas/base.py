from enum import Enum
from typing import Annotated, Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel
from sqlalchemy import Select, desc

T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
  model_config = ConfigDict(alias_generator=to_camel)

  limit: int
  offset: int
  total_count: int
  data: list[T]


class SortOrderEnum(Enum):
  asc = "asc"
  desc = "desc"


class GetListQueryParams(BaseModel):
  limit: Annotated[
    int,
    Query(description="取得するデータの最大取得数", ge=1, le=100, default=10),
  ]
  offset: Annotated[
    int,
    Query(description="取得するタスクのページ数", ge=0, default=0),
  ]
  sort_order: Annotated[
    SortOrderEnum,
    Query(description="取得するタスクのソート順", default=SortOrderEnum.desc.value),
  ]
  """GETリクエストのクエリパラメータを表すクラス"""


class SortTypeEnum(Enum):
  asc: str = "asc"
  desc: str = "desc"


class SortQueryIn(BaseModel):
  sort_field: any | None = Query(None)
  sort_type: SortTypeEnum = Query(SortTypeEnum.asc)

  def apply_to_query(self, query: Select, order_by: any | None = None) -> any:
    if not order_by:
      return query

    if self.sort_type == SortTypeEnum.desc:
      return query.order_by(desc(order_by))
    else:
      return query.order_by(order_by)


class PagingQueryIn(BaseModel):
  page: int = Query(1)
  per_page: int = Query(30)

  @field_validator("page", mode="before")
  def validate_page(cls, v: int) -> int:
    return 1 if not v >= 1 else v

  @field_validator("per_page", mode="before")
  def validate_per_page(cls, v: int) -> int:
    return 30 if not v >= 1 else v

  def get_offset(self) -> int:
    return (
      (self.page - 1) * self.per_page if self.page >= 1 and self.per_page >= 1 else 0
    )

  def apply_to_query(self, query: Select) -> any:
    offset = self.get_offset()
    return query.offset(offset).limit(self.per_page)
