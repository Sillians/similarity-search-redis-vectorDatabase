# If needed, for training new embeddings

import os
from redis.commands.search.field import TagField, TextField, NumericField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

from src.utils.config import get_config
from src.utils.logger import get_logger
from src.utils.redis_client import client_redis
from src.models.embedding_model import vector_embedding, vector_dimension

config = get_config()
logger = get_logger("Create the Redis Search Index for the bikes collection")


VECTOR_DIMENSION = vector_dimension()
client = client_redis()


def create_redis_search_index():
    logger.info("Creates the Redis Search Index for the bikes collection")

    try:
        logger.info("check to see if index exists")
        client.ft(config.INDEX_NAME).info()
        logger.info('Index already exists!')
    except:
        logger.info("Define the schema...")
        schema = (
            TextField('$.model', no_stem=True, as_name='model'),
            TextField('$.brand', no_stem=True, as_name='brand'),
            NumericField('$.price', as_name='price'),
            TagField('$.type', as_name='type'),
            TextField('$.description', as_name='description'),
            VectorField('$.description_embeddings',
                        'FLAT', {
                            'TYPE': 'FLOAT32',
                            'DIM': VECTOR_DIMENSION,
                            'DISTANCE_METRIC': 'COSINE',
                        }, as_name='vector'
                        ),
        )

        logger.info("Index Definition...")
        definition = IndexDefinition(prefix=[config.DOC_PREFIX], index_type=IndexType.JSON)
        try:
            res = client.ft(config.INDEX_NAME).create_index(fields=schema, definition=definition)
            logger. info("Index created.")
            return res
        except Exception as e:
            print("{}, continue with the rest of the program.".format(e))


def check_state_index():
    logger.info("Example check for the state of the index")
    info = client.ft(config.INDEX_NAME).info()

    num_docs = info['num_docs']
    indexing_failures = info['hash_indexing_failures']
    total_indexing_time = info['total_indexing_time']
    percent_indexed = int(info['percent_indexed']) * 100

    return (f"{num_docs} documents ({percent_indexed} percent) indexed with {indexing_failures} failures in {float(total_indexing_time):.2f} milliseconds")



if __name__ == "__main__":
    create_redis_search_index()
    check_ = check_state_index()
    print(check_)







