# Third Party Library
import redis

# Project Library
from project.configs.project_config import config
from project.core.utils.exceptions import ConnectionException

redis_url = config.get(section="redis", key="url")


class RedisConnection:
    def __init__(self):
        try:
            self.redis_instance = redis.Redis.from_url(redis_url)
        except redis.exceptions.ConnectionError as err:
            raise ConnectionException(f"Failed to connect Redis with exception: {err}")


redis_obj = RedisConnection()
