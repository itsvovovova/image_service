import psycopg2
from src.config import get_settings
# Подключение к базе данных
connection = psycopg2.connect(
    dbname=get_settings().postgres_db,
    user=get_settings().postgres_user,
    password=get_settings().postgres_password,
    host=get_settings().postgres_host,
    port=get_settings().postgres_port
)

cursor = connection.cursor()

# Создание базы данных
cursor.execute("CREATE DATABASE "
               "task(uuid VARCHAR(36), "
               "photo BYTEA(250), "
               "filter VARCHAR(100), "
               "status VARCHAR(100), "
               "result BYTEA(250));")

connection.commit()
connection.close()





