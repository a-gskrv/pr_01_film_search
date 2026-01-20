from functools import lru_cache

from app.core.services import FilmSearchService
from app.core.services import QueryLogService


@lru_cache
def get_film_service():
    fs_service = FilmSearchService()
    return fs_service


@lru_cache
def get_log_service():
    q_service =QueryLogService()
    return q_service
