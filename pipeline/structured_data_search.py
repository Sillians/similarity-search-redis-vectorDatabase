# from IPython.display import display, HTML
import os
import numpy as np
import pandas as pd
from typing import List
from dotenv import load_dotenv
from redis.commands.search.query import Query
load_dotenv()

from redis_client import client_redis
from pretrained_model import model

INDEX_NAME=os.getenv('INDEX_NAME')
DOC_PREFIX=os.getenv('DOC_PREFIX')
client = client_redis()
embedder = model()


# # Retrieve all bikes where the brand is Peaknetic
# query = (
#     Query('@brand:Peaknetic').return_fields('id', 'brand', 'model', 'price')
# )
# print(client.ft(INDEX_NAME).search(query).docs)
#
#
# # Get  bikes under $1000
# query = (
#     Query('@brand:Peaknetic @price:[0 1000]').return_fields('id', 'brand', 'model', 'price')
# )
# print(client.ft(INDEX_NAME).search(query).docs)


def semantic_search_vss(queries: List = None):
    encoded_queries = embedder.encode(queries)

    query = (
        Query('(*)=>[KNN 3 @vector $query_vector AS vector_score]')
        .sort_by('vector_score')
        .return_fields('vector_score', 'id', 'brand', 'model', 'description')
        .dialect(2)
    )
    return encoded_queries, query



def create_query_table(query, queries, encoded_queries, extra_params = {}):
    results_list = []
    for i, encoded_query in enumerate(encoded_queries):
        result_docs = client.ft(INDEX_NAME).search(query, { 'query_vector': np.array(encoded_query, dtype=np.float32).tobytes() } | extra_params).docs
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

    # Pretty-print the table
    queries_table = pd.DataFrame(results_list)
    queries_table.sort_values(by=['query', 'score'], ascending=[True, False], inplace=True)
    queries_table['query'] = queries_table.groupby('query')['query'].transform(lambda x: [x.iloc[0]] + ['']*(len(x)-1))
    queries_table['description'] = queries_table['description'].apply(lambda x: (x[:497] + '...') if len(x) > 500 else x)
    return queries_table.to_markdown(index=False)
    # html = queries_table.to_html(index=False)
    # print(display(HTML(html)))


if __name__ == "__main__":

    queries = [
        'Bike for small kids',
        'Best Mountain bikes for kids',
        'Cheap Mountain bike for kids',
        'Female specific mountain bike',
        'Road bike for beginners',
        'Commuter bike for people over 60',
        'Comfortable commuter bike',
        'Good bike for college students',
        'Mountain bike for beginners',
        'Vintage bike',
        'Comfortable city bike'
    ]

    encoded_queries, query = semantic_search_vss(queries)
    print(create_query_table(query, queries, encoded_queries))
