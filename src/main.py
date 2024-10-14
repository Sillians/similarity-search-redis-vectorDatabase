import sys
import unittest
import argparse
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

    def display_query_options(self):
        print("\nPlease choose a query from the list below:")
        for i, query in enumerate(self.queries, start=1):
            print(f"{i}. {query}")
        print("\nEnter the number corresponding to your choice:")

    def get_user_query(self):
        while True:
            try:
                choice = int(input())
                if 1 <= choice <= len(self.queries):
                    return self.queries[choice - 1]
                else:
                    print(f"Invalid input. Please enter a number between 1 and {len(self.queries)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def run(self):

        RedisVectorOperations().pipeline_redis()
        RedisVectorOperations().add_vectorized_description()
        RedisSearchIndex().create_redis_search_index()
        print(RedisSearchIndex().check_state_index())

        self.display_query_options()
        user_query = self.get_user_query()

        print(f"\nYou selected: {user_query}")
        encoded_queries, query = self.semantic_search.semantic_search_vss([user_query])
        result_table = self.semantic_search.create_query_table(query, [user_query], encoded_queries)
        print(result_table)

def main():
    parser = argparse.ArgumentParser(description="Run Semantic Search App or Tests")
    parser.add_argument('--test', action='store_true', help="Run the test cases instead of the main application")
    args = parser.parse_args()

    if args.test:
        # Run unittests if --test flag is provided
        print("Running test cases...")
        unittest.TextTestRunner().run(unittest.defaultTestLoader.discover('tests'))
    else:
        # Run the main application
        print("Running main application...")
        vss = SemanticSearchApp()
        vss.run()


if __name__ == "__main__":
    # vss = SemanticSearchApp()
    # vss.run()
    main()
