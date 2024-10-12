from dotenv import load_dotenv
load_dotenv()

from typing import List, Any
from redis_client import client_redis
from data_processing import data, json_data_to_dataframe
from pretrained_model import vector_embedding


# Storing the Bikes as JSON Documents in Redis
def pipeline_redis() -> Any:
    client = client_redis()
    bikes = data()
    pipeline = client.pipeline()

    for i, bike in enumerate(bikes, start=1):
        redis_key = f'bikes:{i:03}'
        pipeline.json().set(redis_key, '$', bike)
    return pipeline.execute()


# Add the vectorized descriptions to the JSON documents in Redis using the JSON.SET
def add_vectorized_description() -> List:
    client = client_redis()
    embeddings = vector_embedding()

    pipeline = client.pipeline()
    keys = sorted(client.keys('bikes:*'))
    for key, embedding in zip(keys, embeddings):
        pipeline.json().set(key, '$.description_embeddings', embedding)
    return pipeline.execute()


if __name__ == "__main__":
    pipeline_redis()
    add_vectorized_description()