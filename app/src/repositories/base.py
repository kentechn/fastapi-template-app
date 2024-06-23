from typing import Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models.base import Base
from src.schemas.base import ModelQueryParams, PagingQueryIn, SortQueryIn

# from src.schemas.base import PagingQueryIn, SortQueryIn

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SortQueryInType = TypeVar("SortQueryInType", bound=SortQueryIn)
ModelQueryParamsType = TypeVar("ModelQueryParamsType", bound=ModelQueryParams)


class BaseRepository(
  Generic[
    ModelType, CreateSchemaType, UpdateSchemaType, SortQueryInType, ModelQueryParamsType
  ]
):
  def __init__(self, model: Type[ModelType]) -> None:
    self.model = model

  def get_db_obj_by_id(self, db: Session, id: int) -> ModelType | None:
    result = db.execute(select(self.model).filter(self.model.id == id))
    return result.scalar_one_or_none()

  def get_db_obj_list(
    self,
    db: Session,
    page_params: PagingQueryIn,
    sort_params: SortQueryInType,
    query_params: ModelQueryParamsType,
  ) -> list[ModelType]:
    stmt = select(self.model)
    stmt = query_params.apply_to_query(stmt)

    # Get total count
    total_count_stmt = select(func.count()).select_from(stmt.subquery())
    total_count = db.execute(total_count_stmt).scalar()

    # Apply sorting
    stmt = sort_params.apply_to_query(stmt)

    # Apply paging
    stmt = page_params.apply_to_query(stmt)

    # Add more conditions for other fields if needed
    data = db.execute(stmt).scalars().all()

    return data, total_count

  def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
    obj_in_data = obj_in.model_dump(by_alias=False)
    db_obj = self.model(**obj_in_data)
    db.add(db_obj)
    db.flush()
    db.refresh(db_obj)
    return db_obj

  def update(
    self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType
  ) -> ModelType:
    # task_updateオブジェクトを辞書に変換し、未設定の値を除外する
    obj_data: dict[str, any] = jsonable_encoder(
      obj_in, by_alias=False, exclude_unset=True
    )

    for field, value in obj_data.items():
      setattr(db_obj, field, value)
    db.flush()
    db.refresh(db_obj)
    return db_obj

  def real_delete(self, db: Session, db_obj: ModelType) -> None:
    db.delete(db_obj)
    db.flush()

    return db_obj
