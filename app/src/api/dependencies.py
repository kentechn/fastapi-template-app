from collections.abc import Generator

from sqlalchemy.orm import Session

from src.core.database import sessionLocal


# Dependency
def get_db() -> Generator[Session, None, None]:
  db = sessionLocal()
  try:
    yield db
    db.commit()
  except Exception as e:
    if db:
      db.rollback()
    raise e
  finally:
    db.close()


# async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
#   """async用のdb-sessionの作成."""
#   async with async_session_factory() as db:
#     try:
#       yield db
#       await db.commit()
#     except Exception:
#       await db.rollback()
#     finally:
#       await db.close()
