from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_engine(settings.mysql_db_url, echo=True)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
