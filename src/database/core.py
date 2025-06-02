from sqlalchemy import create_engine, MetaData
from logging import getLogger
from src.config import get_settings
from sqlalchemy.orm import sessionmaker

from src.database.models import Base

log = getLogger(__name__)

# Создаем метаданные
meta_data = MetaData()

# Подключаемся к уже существующей бд
engine = create_engine(get_settings().database_url)
log.info("The database is connected")

Session = sessionmaker(autoflush=False, bind=engine)










