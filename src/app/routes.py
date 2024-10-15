from typing import List
from fastapi import APIRouter, HTTPException
from src.pipelines.inference_pipeline import SemanticSearch
from src.data.vector_store import RedisVectorOperations
from src.pipelines.training_pipeline import RedisSearchIndex
from src.utils.logger import get_logger

log = get_logger("Semantic Search on Bikes dataset...")

router = APIRouter()

log.info("Initialize the search app and index setup")
search_app = SemanticSearch()
RedisVectorOperations().pipeline_redis()
RedisVectorOperations().add_vectorized_description()
RedisSearchIndex().create_redis_search_index()

@router.post("/search/")
def search_bikes(query: str):
    """
    Perform a semantic search on the bikes dataset.
    - `query`: Search query input from the user
    """
    try:
        encoded_queries, result_query = search_app.semantic_search_vss([query])
        result_table = search_app.create_query_table(result_query, [query], encoded_queries)
        return {"query": query, "results": result_table}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {e}")


@router.get("/queries/")
def get_available_queries():
    """
    Get the list of predefined search queries
    to help users understand what kind of searches can be performed.
    """
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
    try:
        return {"available_queries": queries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving queries: {e}")


@router.post("/search/paginated/")
def search_bikes_paginated(query: str, page: int = 1, per_page: int = 10):
    """
    Perform a paginated semantic search on the bikes dataset.
    - `query`: Search query input from the user.
    - `page`: Page number (default: 1).
    - `per_page`: Results per page (default: 10).
    """
    try:
        encoded_queries, result_query = search_app.semantic_search_vss([query])
        result_table = search_app.create_query_table(result_query, [query], encoded_queries)

        # pagination logic
        start = (page - 1) * per_page
        end = start + per_page
        paginated_results = result_table[start:end]

        return {
            "query": query,
            "page": page,
            "per_page": per_page,
            "results": paginated_results,
            "total_results": len(result_table)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {e}")


@router.post("/refresh-index/")
def refresh_search_index():
    """
    Rebuild the Redis search index.
    """
    try:
        RedisSearchIndex().create_redis_search_index()
        return {"message": "Search index refreshed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing search index: {e}")


@router.post("/batch-search/")
def batch_search_bikes(queries: List[str]):
    """
    Perform a semantic search on a batch of queries.
    - `queries`: List of search queries from the user.
    """
    try:
        encoded_queries, result_query = search_app.semantic_search_vss(queries)
        result_table = search_app.create_query_table(result_query, queries, encoded_queries)
        return {"batch_results": result_table}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing batch search: {e}")


























































































