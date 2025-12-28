from collections.abc import Callable
from typing import Dict, Any

from app.core import services

# from pprint import pprint

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

# pprint(ACTION_REGISTRY)

#
# dict_main_menu = {
#     "0": {"name": "EXIT.", "func": exit},
#     "1": {"name": "Найти фильм по ключевому слову.", "func": search_film.search_film_keyword},
#     "2": {"name": "Найти фильм по жанру и диапазону годов выпуска.", "func": search_film.search_film_category_year},
#     "3": {"name": "Найти фильм по жанру.", "func": search_film.search_film_category},
#     "4": {"name": "Найти фильм по диапазону годов выпуска.", "func": search_film.search_film_year},
#     "5": {"name": "Посмотреть ТОП самых популярных запросов.", "func": get_queries.get_queries_top_search},
#     "6": {"name": "Посмотреть последние уникальные запросы.", "func": get_queries.get_queries_recent_unique},