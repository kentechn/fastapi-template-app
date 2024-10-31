from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, CommonColumns, int_pk, str_255


# Userテーブル
class User(Base, CommonColumns):
  __tablename__ = "user"

  id: Mapped[int_pk] = mapped_column(comment="ユーザーID")
  is_admin: Mapped[Boolean] = mapped_column(
    Boolean, default=False, comment="管理者権限"
  )
  username: Mapped[str_255] = mapped_column(comment="ユーザー名")
  hashed_password: Mapped[str_255] = mapped_column(comment="ハッシュ化パスワード")

  tasks = relationship(
    "Task", back_populates="create_user", cascade="all, delete-orphan"
  )

  def __repr__(self) -> str:
    return f"User(id={self.id!r}, username={self.username!r})"
