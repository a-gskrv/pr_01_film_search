from collections.abc import Callable
from typing import Any

from app.core.services import FilmSearchService
from app.core.query_log_service import QueryLogService


ACTION_REGISTRY: dict[str, dict[str, Any]] = {}


def register_action(action_id: str, title: str, handler: Callable[..., Any], parameters: list[str]) -> None:
    """
    Register an action in the global action registry.

    Args:
        action_id: Unique action identifier.
        title: Human-readable action title.
        handler: Callable handler for the action.
        parameters: List of parameter names required for the action.
    """
    ACTION_REGISTRY[action_id] = {
        "id": action_id,
        "title": title,
        "handler": handler,
        "parameters": parameters,
    }


# --- Film search actions ---
register_action(
    action_id="search_by_keyword",
    title="Search films by keyword",
    handler=FilmSearchService().search_by_keyword,
    parameters=["keyword"],
)

register_action(
    action_id="search_by_category",
    title="Search films by category",
    handler=FilmSearchService().search_by_category,
    parameters=["dict_category"],
)

register_action(
    action_id="search_by_category_year",
    title="Search films by category and year range",
    handler=FilmSearchService().search_by_category_year,
    parameters=["dict_category", "year_from", "year_to"],
)


# --- Reports ---
register_action(
    action_id="report_last_unique_queries",
    title="Report: last 5 unique queries",
    handler=QueryLogService().get_last_unique_queries,
    parameters=[],
)

register_action(
    action_id="report_top_queries",
    title="Report: top 5 most frequent queries",
    handler=QueryLogService().get_top_queries,
    parameters=[],
)
