from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import get_settings

settings = get_settings()


engine = create_engine(settings.mysql_db_url, echo=True)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
