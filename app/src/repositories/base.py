from typing import Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
  def __init__(self, model: Type[ModelType]) -> None:
    self.model = model

  def get_db_obj_by_id(self, db: Session, id: int) -> ModelType | None:
    result = db.execute(select(self.model).filter(self.model.id == id))
    return result.scalar_one_or_none()

  def get_db_obj_list(
    self, db: Session, offset: int = 0, limit: int = 10
  ) -> list[ModelType]:
    result = db.execute(select(self.model).offset(offset).limit(limit))
    return result.scalars().all()

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
