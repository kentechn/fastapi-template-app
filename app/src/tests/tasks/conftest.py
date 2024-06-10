import pytest
from sqlalchemy.orm import Session

from src.models.task import Task


@pytest.fixture(scope="function")
def insert_tasks(db: Session) -> None:
  test_data = [
    Task(content="test content"),
    Task(content="test content"),
    Task(content="test content"),
  ]

  db.add_all(test_data)
  db.flush()

  return test_data
