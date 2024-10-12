# Handling Redis vector operations
from typing import List, Any
from src.utils.redis_client import RedisClient
from src.data.data_loader import BikeDataLoader
from src.models.embedding_model import VectorEmbedding
from src.utils.logger import get_logger
from src.utils.config import get_config

class RedisVectorOperations:
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger("Handling Redis Vector Operations...")
        self.client = RedisClient().connect()
        self.logger.info("Get the embedder model, Redis client, and the bikes data...")
        self.embeddings = VectorEmbedding().vector_embedding()
        self.bikes = BikeDataLoader().load_data()

    def pipeline_redis(self) -> Any:
        self.logger.info("Storing the Bikes as JSON Documents in Redis")
        pipeline = self.client.pipeline()
        for i, bike in enumerate(self.bikes, start=1):
            redis_key = f'{self.config.DOC_PREFIX}:{i:03}'
            pipeline.json().set(redis_key, '$', bike)
        self.logger.info("Executing the pipeline to store the bikes as JSON documents...")
        return pipeline.execute()

    def add_vectorized_description(self) -> List:
        self.logger.info("Adding vectorized descriptions to the JSON documents in Redis using JSON.SET")
        pipeline = self.client.pipeline()
        keys = sorted(self.client.keys(self.config.CLIENT_KEYS))
        for key, embedding in zip(keys, self.embeddings):
            pipeline.json().set(key, '$.description_embeddings', embedding)
        self.logger.info("Executing the pipeline to add vectorized descriptions...")
        return pipeline.execute()


