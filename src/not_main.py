from src.pipelines.inference_pipeline import SemanticSearch
from src.data.vector_store import RedisVectorOperations
from src.pipelines.training_pipeline import RedisSearchIndex

class SemanticSearchApp:
    def __init__(self):
        self.queries = [
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
        self.semantic_search = SemanticSearch()

    def run(self):
        RedisVectorOperations().pipeline_redis()
        RedisVectorOperations().add_vectorized_description()
        RedisSearchIndex().create_redis_search_index()
        print(RedisSearchIndex().check_state_index())

        encoded_queries, query = self.semantic_search.semantic_search_vss(self.queries)
        result_table = self.semantic_search.create_query_table(query, self.queries, encoded_queries)
        print(result_table)

if __name__ == "__main__":
    vss = SemanticSearchApp()
    vss.run()