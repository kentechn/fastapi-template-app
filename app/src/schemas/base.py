from enum import Enum
from typing import Any, Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel
from sqlalchemy import Select, asc, desc

T = TypeVar("T")


class BaseSchema(BaseModel):
  """レスポンスの基底クラス"""

  model_config = ConfigDict(
    alias_generator=to_camel,
    use_enum_values=True,
    populate_by_name=True,
    arbitrary_types_allowed=True,
    strict=True,
  )


class ListResponse(BaseModel, Generic[T]):
  model_config = ConfigDict(alias_generator=to_camel)

  page: int
  size: int
  total_count: int
  data: list[T]


class SortTypeEnum(Enum):
  asc: str = "asc"
  desc: str = "desc"


class SortQueryIn(BaseModel):
  sort_by: Any = Query(None)
  sort_type: SortTypeEnum = Query(SortTypeEnum.desc)

  model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)

  def apply_to_query(self, query: Select) -> Select:
    if not self.sort_by:
      return query

    if self.sort_type == SortTypeEnum.desc.value:
      return query.order_by(desc(self.sort_by))
    else:
      return query.order_by(asc(self.sort_by))


class PagingQueryIn(BaseModel):
  size: int = Query(10, ge=1, description="1ページあたりの表示数")
  page: int = Query(1, ge=1, description="ページ番号")

  @property
  def offset(self) -> int:
    return (self.page - 1) * self.size

  def apply_to_query(self, query: Select) -> Select:
    return query.offset(self.offset).limit(self.size)


class ModelQueryParams(BaseModel):
  model_config = ConfigDict(alias_generator=to_camel, use_enum_values=True)

  def apply_to_query(self, query: Select) -> Select:
    return query
