from collections.abc import Callable
from typing import Dict, Any

from app.core import services

ACTION_REGISTRY: Dict[str, dict[str, Any]] = {}


def register_action(action_id: str, title: str, handler: Callable, parameters: list[str],) -> None:

    ACTION_REGISTRY[action_id] = {
        "id": action_id,
        "title": title,
        "handler": handler,
        "parameters": parameters,
    }

register_action(
    action_id="search_by_keyword",
    title="Search films by keyword",
    handler=services.search_by_keyword,
    parameters=["keyword", "limit", "offset"],
)

register_action(
    action_id="search_by_category_year",
    title="Search films by category and year range",
    handler=services.search_by_category_year,
    parameters=["category", "year", "limit", "offset"],
)

register_action(
    action_id="search_by_category",
    title="Search films by category",
    handler=services.search_by_category,
    parameters=["category", "limit", "offset"],
)

register_action(
    action_id="search_by_year",
    title="Search films by year range",
    handler=services.search_by_year,
    parameters=["year", "limit", "offset"],
)
