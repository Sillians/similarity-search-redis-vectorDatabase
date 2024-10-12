# Entry point for running pipelines or tasks
from src.pipelines.inference_pipeline import SemanticSearch


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

    vss = SemanticSearch()
    encoded_queries, query = vss.semantic_search_vss(queries)
    print(vss.create_query_table(query, queries, encoded_queries))