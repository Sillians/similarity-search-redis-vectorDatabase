import os
from redis.commands.search.field import TagField, TextField, NumericField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
# from src.core.logger import *
from dotenv import load_dotenv
load_dotenv()

from redis_client import client_redis
from pretrained_model import vector_dimension, vector_embedding

# log = Logger("Create the Redis Search Index for the bikes collection", logging.INFO).get_logger()

INDEX_NAME=os.getenv('INDEX_NAME')
DOC_PREFIX=os.getenv('DOC_PREFIX')
VECTOR_DIMENSION = vector_dimension()
client = client_redis()

# creates the Redis Search Index for the bikes collection
def create_redis_search_index():

    try:
        # check to see if index exists
        client.ft(INDEX_NAME).info()
        # log.info('Index already exists!')
    except:
        # schema
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

        # index Definition
        definition = IndexDefinition(prefix=[DOC_PREFIX], index_type=IndexType.JSON)
        # create Index
        try:
            res = client.ft(INDEX_NAME).create_index(fields=schema, definition=definition)
            return res
        except Exception as e:
            print("{}, continue with the rest of the program.".format(e))


def check_state_index():
    # Check the state of the index
    info = client.ft(INDEX_NAME).info()

    num_docs = info['num_docs']
    indexing_failures = info['hash_indexing_failures']
    total_indexing_time = info['total_indexing_time']
    percent_indexed = int(info['percent_indexed']) * 100

    return (f"{num_docs} documents ({percent_indexed} percent) indexed with {indexing_failures} failures in {float(total_indexing_time):.2f} milliseconds")



if __name__ == "__main__":
    create_redis_search_index()
    check_ = check_state_index()
    print(check_)







