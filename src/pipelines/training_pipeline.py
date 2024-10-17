# If needed, for training new embeddings
from redis.commands.search.field import TagField, TextField, NumericField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from src.utils.config import get_config
from src.utils.logger import get_logger
from src.utils.redis_client import RedisClient
from src.models.embedding_model import VectorEmbedding

class RedisSearchIndex:
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger("Redis Search Index for the bikes collection")
        self.vector_dimension = VectorEmbedding().vector_dimension()
        self.client = RedisClient().connect()

    def create_redis_search_index(self):
        self.logger.info("Creating the Redis Search Index for the bikes collection")

        try:
            self.logger.info("Checking if the index already exists...")
            self.client.ft(self.config.INDEX_NAME).info()
            self.logger.info('Index already exists!')
        except:
            self.logger.info("Defining the schema...")
            schema = (
                TextField('$.model', no_stem=True, as_name='model'),
                TextField('$.brand', no_stem=True, as_name='brand'),
                NumericField('$.price', as_name='price'),
                TagField('$.type', as_name='type'),
                TextField('$.description', as_name='description'),
                VectorField('$.description_embeddings',
                            'FLAT', {
                                'TYPE': 'FLOAT32',
                                'DIM': self.vector_dimension,
                                'DISTANCE_METRIC': 'COSINE',
                            }, as_name='vector'
                            ),
            )

            self.logger.info("Setting up the index definition...")
            definition = IndexDefinition(prefix=[self.config.DOC_PREFIX], index_type=IndexType.JSON)
            try:
                res = self.client.ft(self.config.INDEX_NAME).create_index(fields=schema, definition=definition)
                self.logger.info("Index created successfully.")
                return res
            except Exception as e:
                self.logger.error(f"Failed to create index: {e}, continuing with the rest of the program.")

    def check_state_index(self):
        self.logger.info("Checking the state of the Redis index")
        info = self.client.ft(self.config.INDEX_NAME).info()

        num_docs = info['num_docs']
        indexing_failures = info['hash_indexing_failures']
        total_indexing_time = info['total_indexing_time']
        percent_indexed = int(info['percent_indexed']) * 100

        return f"{num_docs} documents ({percent_indexed} percent) indexed with {indexing_failures} failures in {float(total_indexing_time):.2f} milliseconds"







