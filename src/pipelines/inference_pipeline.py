import numpy as np
import pandas as pd
from typing import List
from redis.commands.search.query import Query
from src.utils.redis_client import RedisClient
from src.models.similarity_model import SimilarityModel
from src.utils.logger import get_logger
from src.utils.config import get_config


class SemanticSearch:
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger("Embedding and Pure KNN VSS Similarity Search")
        self.client = RedisClient().connect()
        self.embedder = SimilarityModel().load_model()

    def semantic_search_vss(self, queries: List = None):
        encoded_queries = self.embedder.encode(queries)

        query = (
            Query('(*)=>[KNN 3 @vector $query_vector AS vector_score]')
            .sort_by('vector_score')
            .return_fields('vector_score', 'id', 'brand', 'model', 'description')
            .dialect(2)
        )
        return encoded_queries, query

    def create_query_table(self, query, queries, encoded_queries, extra_params={}):
        results_list = []
        for i, encoded_query in enumerate(encoded_queries):
            result_docs = self.client.ft(self.config.INDEX_NAME).search(
                query, {'query_vector': np.array(encoded_query, dtype=np.float32).tobytes()} | extra_params
            ).docs

            for doc in result_docs:
                vector_score = round(1 - float(doc.vector_score), 2)
                results_list.append({
                    'query': queries[i],
                    'score': vector_score,
                    'id': doc.id,
                    'brand': doc.brand,
                    'model': doc.model,
                    'description': doc.description
                })

        self.logger.info("Pretty-printing the table")
        queries_table = pd.DataFrame(results_list)
        queries_table.sort_values(by=['query', 'score'], ascending=[True, False], inplace=True)
        queries_table['query'] = queries_table.groupby('query')['query'].transform(
            lambda x: [x.iloc[0]] + [''] * (len(x) - 1))
        queries_table['description'] = queries_table['description'].apply(
            lambda x: (x[:497] + '...') if len(x) > 500 else x)
        return queries_table.to_markdown(index=False)

