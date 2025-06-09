from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from logging import getLogger
from src.config import get_settings

log = getLogger(__name__)

database_url = get_settings().database_url

engine = create_engine(database_url)

if not database_exists(engine.url):
    create_database(engine.url)
    log.info("Database did not exist — created new one.")
else:
    log.info("Database already exists.")

meta_data = MetaData()
Session = sessionmaker(autoflush=False, bind=engine)