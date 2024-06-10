from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import text
from typing_extensions import Annotated

# 型の作成
int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_255 = Annotated[str, mapped_column(String(255))]
str_10 = Annotated[str, mapped_column(String(10))]
timestamp = Annotated[
  datetime,
  mapped_column(DateTime(timezone=True), server_default=text("NOW()")),
]


class Base(DeclarativeBase):
  pass


# テーブル共通カラム
class CommonColumns:
  created_at: Mapped[timestamp] = mapped_column(comment="作成日時")
  updated_at: Mapped[timestamp] = mapped_column(
    onupdate=text("NOW()"), comment="更新日時"
  )
