# Handling Redis vector operations
from dotenv import load_dotenv
load_dotenv()

from typing import List, Any
from src.utils.redis_client import client_redis
from src.data.data_loader import data, json_data_to_dataframe
from src.models.embedding_model import vector_embedding
from src.utils.logger import get_logger
from src.utils.config import get_config

config = get_config()
logger = get_logger("Handling Redis Vector Operations...")

logger.info("Get the embedder model, redis client and the bikes data...")
client = client_redis()
embeddings = vector_embedding()
bikes = data()

def pipeline_redis() -> Any:
    logger.info("Storing the Bikes as JSON Documents in Redis")
    pipeline = client.pipeline()
    for i, bike in enumerate(bikes, start=1):
        redis_key = f'{config.DOC_PREFIX}:{i:03}'
        pipeline.json().set(redis_key, '$', bike)
    logger.info("Executes the pipeline to store the bikes as JSON documents...")
    return pipeline.execute()


def add_vectorized_description() -> List:
    logger.info("Add the vectorized descriptions to the JSON documents in Redis using the JSON.SET")
    pipeline = client.pipeline()
    keys = sorted(client.keys(config.CLIENT_KEYS))
    for key, embedding in zip(keys, embeddings):
        pipeline.json().set(key, '$.description_embeddings', embedding)
    logger.info("Executes the pipeline to add vectorized descriptions...")
    return pipeline.execute()


# if __name__ == "__main__":
#     pipeline_redis()
#     add_vectorized_description()
