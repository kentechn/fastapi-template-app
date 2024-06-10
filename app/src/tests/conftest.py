from collections.abc import Generator
from typing import Any

import pymysql
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.api.dependencies import get_db
from src.main import app

mysql_db_url = "mysql+pymysql://root:root@db:3306/test"
engine = create_engine(mysql_db_url, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.rollback()
    db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> None:
  """
  テスト用データベースを作成するフィクスチャ
  """

  conn = pymysql.connect(host="db", user="root", password="root", port=3306)
  cursor = conn.cursor()

  cursor.execute("SHOW DATABASES LIKE 'test'")
  result = cursor.fetchone()

  if not result:
    cursor.execute("CREATE DATABASE test")


@pytest.fixture(scope="function")
def test_client(db: Session) -> Generator[TestClient, Any, None]:
  def override_get_db() -> Generator[Session, None, None]:
    yield db

  app.dependency_overrides[get_db] = override_get_db
  with TestClient(app) as client:
    yield client
