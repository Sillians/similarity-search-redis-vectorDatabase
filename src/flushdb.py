from src.utils.redis_client import RedisClient
from src.utils.logger import get_logger
logger = get_logger("Flush the Vector Database, and remove all keys from the Database")

def flush_redis_database():
    client = RedisClient().connect()
    try:
        client.flushdb()
        logger.info("Successfully flushed the current Redis database.")
    except Exception as e:
        logger.error(f"Error flushing Redis database: {e}")

if __name__ == "__main__":
    flush_redis_database()
