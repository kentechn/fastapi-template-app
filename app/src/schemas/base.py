from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
  limit: int
  offset: int
  total_count: int
  data: list[T]


class GetListQueryParams(BaseModel):
  limit: int = Query(100, description="取得するタスクの最小, 最大数", ge=1, le=100)
  offset: int = Query(0, description="取得するタスクのオフセット", ge=0)
  """GETリクエストのクエリパラメータを表すクラス"""
