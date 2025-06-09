from redis import Redis
from src.config import get_settings

current_connection = Redis(host="host.docker.internal", port=get_settings().redis_port)

