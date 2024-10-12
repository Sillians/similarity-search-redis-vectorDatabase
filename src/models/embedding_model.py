import numpy as np
from textwrap import TextWrapper
from typing import Any
from src.utils.redis_client import client_redis
from src.data.data_loader import data
from src.models.similarity_model import model
from src.utils.logger import get_logger
from src.utils.config import get_config

config = get_config()
logger = get_logger("Vector embedding and vector dimension generation")

logger.info("Load the embedder model, redis client and the bikes data...")
embedder = model()
client = client_redis()
bikes = data()

def vector_embedding() -> Any:
    logger.info("Vectorize all of the Bikes Descriptions")
    keys = sorted(client.keys(config.CLIENT_KEYS))
    descriptions = client.json().mget(keys, '$.description')
    descriptions = [item for sublist in descriptions for item in sublist]
    embeddings = embedder.encode(descriptions).astype(np.float32).tolist()
    logger.info("vector embeddings of all the Bikes descriptions")
    return embeddings


def vector_dimension() -> int:
    logger.info("Extract the length of the vector embeddings generated by the model")
    sample_description = bikes[0]['description']
    TextWrapper(width=120).wrap(sample_description)
    embedding = embedder.encode(sample_description)
    VECTOR_DIMENSION = len(embedding)
    logger.info("length of the vector dimension embeddings generated by the model")
    return VECTOR_DIMENSION


# if __name__ == "__main__":
#     vector_embedding()
#     vd = vector_dimension()
#     print(vd)