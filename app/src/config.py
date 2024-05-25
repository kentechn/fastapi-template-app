import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  mysql_host: str = os.getenv("MYSQL_HOST")
  mysql_port: int = os.getenv("MYSQL_PORT")
  mysql_user: str = os.getenv("MYSQL_USER")
  mysql_password: str = os.getenv("MYSQL_PASSWORD")
  mysql_db: str = os.getenv("MYSQL_DATABASE")
  mysql_db_url: str = os.getenv("MYSQL_DATABASE_URL")


@lru_cache
def get_settings() -> Settings:
  return Settings()
