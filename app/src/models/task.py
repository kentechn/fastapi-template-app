from sqlalchemy import Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, CommonColumns, int_pk


# Taskテーブル
class Task(Base, CommonColumns):
  __tablename__ = "task"

  id: Mapped[int_pk] = mapped_column(comment="タスクID")
  is_completed: Mapped[Boolean] = mapped_column(
    Boolean, default=False, comment="完了フラグ"
  )
  content: Mapped[str] = mapped_column(Text, comment="タスク内容")
