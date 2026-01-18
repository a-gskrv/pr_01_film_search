from typing import Any

QUERY_LOGS_COLLECTION_NAME = "final_project_010825_albert"

def build_top_queries_pipeline(limit: int = 5) -> list[dict[str, Any]]:
    """Build MongoDB aggregation pipeline for top search queries."""
    return [
        {"$addFields": {"params.search_type": "$search_type"}},
        {"$group": {"_id": "$params", "count_query": {"$sum": 1}}},
        {"$addFields": {"_id.count_query": "$count_query"}},
        {"$sort": {"count_query": -1}},
        {"$replaceRoot": {"newRoot": "$_id"}},
        {"$limit": limit},
    ]


def build_last_unique_queries_pipeline(limit: int = 200) -> list[dict[str, Any]]:
    """Build MongoDB aggregation pipeline for last unique queries."""
    return [
        {
            "$addFields": {
                "params.search_type": "$search_type",
                "params.timestamp": "$timestamp",
            }
        },
        {"$replaceRoot": {"newRoot": "$params"}},
        {"$sort": {"timestamp": -1}},
        {"$limit": limit},
    ]
