import redis
from src.utils.logger import get_logger
from src.utils.config import get_config

config = get_config()
logger = get_logger("Create connection to Redis database client")


# Define the Redis client
def client_redis() -> None:
    try:
        client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            password=config.REDIS_PASSWORD
        )
        logger.info("connection to the redis database client successful.")
        return client
    except Exception as e:
        logger.error(f"errror connecting to the redis database client {e}")