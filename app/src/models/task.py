from sqlalchemy import Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, CommonColumns, int_pk


# Taskテーブル
class Task(Base, CommonColumns):
  __tablename__ = "task"

  id: Mapped[int_pk] = mapped_column(comment="タスクID")
  is_completed: Mapped[Boolean] = mapped_column(
    Boolean, default=False, comment="完了フラグ"
  )
  content: Mapped[str] = mapped_column(Text, comment="タスク内容")

  create_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
  create_user = relationship("User", back_populates="tasks")


  def __repr__(self) -> str:
    return f"Task(id={self.id!r}, content={self.content!r})"