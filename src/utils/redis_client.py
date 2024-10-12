import redis
from src.utils.logger import get_logger
from src.utils.config import get_config

class RedisClient:
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger("Redis Database Client")
        self.client = None

    def connect(self) -> redis.Redis:
        try:
            self.client = redis.Redis(
                host=self.config.REDIS_HOST,
                port=self.config.REDIS_PORT,
                password=self.config.REDIS_PASSWORD
            )
            self.logger.info("Connection to the Redis database client successful.")
            return self.client
        except Exception as e:
            self.logger.error(f"Error connecting to the Redis database client: {e}")
