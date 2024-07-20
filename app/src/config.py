import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  mysql_host: str = os.getenv("MYSQL_HOST")
  mysql_port: str = os.getenv("MYSQL_PORT")
  mysql_user: str = os.getenv("MYSQL_USER")
  mysql_password: str = os.getenv("MYSQL_PASSWORD")
  mysql_db: str = os.getenv("MYSQL_DATABASE")
  mysql_db_url: str = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"

  app_root_path: str = "/api"


@lru_cache
def get_settings() -> Settings:
  return Settings()


settings = get_settings()
