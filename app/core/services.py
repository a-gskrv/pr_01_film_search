from collections import defaultdict
from datetime import datetime
from typing import Optional, Any, Tuple

from pymongo.errors import PyMongoError

from app.core.db.connection import get_mysql_connection
from app.core.db.mongo_connection import get_mongo_db
from app.core.repositories import films_mysql_repo as repo
from app.core.repositories import query_logs_mongo_repo as repo_mogo

name_log_collection = repo_mogo.QUERY_LOGS_COLLECTION_NAME


def calculate_total_pages(total: int, page_size: int) -> int:
    """
    Calculate the total number of pages for paginated results.

    Args:
        total: Total number of items.
        page_size: Number of items per page.

    Returns:
        int: Total number of pages (0 if total is 0).
    """
    if total > 0:
        pages = (total + page_size - 1) // page_size
    else:
        pages = 0
    return pages


def get_text_query(item: dict) -> str:
    """
        Build a human-readable query text based on a logged search record.

        Args:
            item: Dictionary containing search log data. Expected keys depend on the search type.

        Returns:
            str: Formatted query text:
                - keyword: "<keyword>"
                - category: "<category>"
                - category_year: "<category> (<years_range>)"
        """
    q_type = item.get('search_type')
    text_query = ''
    if q_type == 'keyword':
        text_query = f"{item.get('keyword')}"
    elif q_type == 'category':
        text_query = f"{item.get('category_name')}"
    elif q_type == 'category_year':
        text_query = f"{item.get('category_name')} ({item.get('years_range')})"
    return text_query


def get_format_date(timestamp: str) -> str:
    """
        Convert an ISO-formatted timestamp string into a human-readable date string.

        Args:
            timestamp: Timestamp string in ISO format (e.g., "2026-01-18T14:30:52.005468").

        Returns:
            str: Formatted date string (e.g., "18.01.2026 14:30:52").
        """
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%d.%m.%Y %H:%M:%S")


def _to_int_or_none(value: Any) -> Optional[int]:
    """Convert value to int, return None if value is empty/invalid."""
    if value is None:
        return None
    if isinstance(value, int):
        return value
    s = str(value).strip()
    if s == "":
        return None
    try:
        return int(s)
    except (TypeError, ValueError):
        return None


def normalize_year_range_for_category(year_from: Any, year_to: Any,
                                      allowed_year_from: int, allowed_year_to: int) -> Tuple[int, int]:
    """
    Normalize user input year range to fit into [allowed_year_from, allowed_year_to].

    Rules:
    - If year_from is missing/invalid -> allowed_year_from
    - If year_to is missing/invalid -> allowed_year_to
    - If year_from < allowed_year_from -> allowed_year_from
    - If year_to > allowed_year_to -> allowed_year_to
    - If after normalization year_from > year_to -> swap (or clamp both to a single year)
    """
    yf = _to_int_or_none(year_from)
    yt = _to_int_or_none(year_to)

    if yf is None:
        yf = allowed_year_from
    if yt is None:
        yt = allowed_year_to

    # clamp into allowed range
    if yf < allowed_year_from:
        yf = allowed_year_from
    if yf > allowed_year_to:
        yf = allowed_year_to

    if yt > allowed_year_to:
        yt = allowed_year_to
    if yt < allowed_year_from:
        yt = allowed_year_from

    # make range valid
    if yf > yt:
        yf, yt = yt, yf

    return yf, yt


class FilmSearchService:
    def __init__(self):
        # self.connection = get_mysql_connection()
        pass

    def search_by_keyword(self, keyword: str, page_size: int = 10, page: int = 1, log: bool = True, **kwargs) -> dict:
        """
    Search films by a keyword in the title.

    The result is returned in a paginated format.

    Args:
        keyword: Keyword to search for.
        page_size: Number of items per page.
        page: Page number (1-based).
        log: If True, writes the search query to analytics logs (only for the first request).

    Returns:
        dict: Paginated response with the following keys:
            - items (list[dict]): list of films, each item contains:
                -- film_id (int)
                -- title (str)
                -- release_year (int)
            - total (int): total matching films
            - page (int): current page number
            - page_size (int): number of items per page
            - pages (int): total number of pages
    """
        # print('services.search_by_keyword',keyword)
        conn = get_mysql_connection()
        # conn = self.connection
        offset = (page - 1) * page_size
        try:
            items = repo.search_films_by_title_like(conn, keyword, page_size, offset)
            total = repo.count_films_by_title_like(conn, keyword)
            pages = calculate_total_pages(total, page_size)

            if log:
                search_type = "keyword"
                lower_keyword = keyword.lower()
                params = {"keyword": lower_keyword, "results_count": total}
                log_search_query(search_type, params)

            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "pages": pages
            }
        finally:
            conn.close()

    def search_by_category(self, dict_category, page_size: int = 10, page: int = 1, log: bool = True, **kwargs) -> dict:
        """
        Search films by a selected category.

        The result is returned in a paginated format.

        Args:
            dict_category: Category info dict containing:
                -- category_id (int)
                -- category_name (str)
            page_size: Number of items per page.
            page: Page number (1-based).
            log: If True, writes the search query to analytics logs (only for the first request).

        Returns:
            dict: Paginated response with the following keys:
                - items (list[dict]): list of films, each item contains:
                    -- film_id (int)
                    -- title (str)
                    -- release_year (int)
                    -- category (str)
                - total (int): total matching films
                - page (int): current page number
                - page_size (int): number of items per page
                - pages (int): total number of pages
        """

        conn = get_mysql_connection()

        offset = (page - 1) * page_size
        category_id = dict_category.get("category_id")
        category_name = dict_category.get("category_name")
        try:
            items = repo.search_films_by_category(conn, category_id, page_size, offset)
            total = repo.count_films_by_category(conn, category_id)
            pages = calculate_total_pages(total, page_size)

            if log:
                search_type = "category"
                params = {"category_name": category_name, "results_count": total}
                log_search_query(search_type, params)

            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "pages": pages
            }
        finally:
            conn.close()

    def search_by_category_year(self, dict_category, year_from, year_to, page_size: int = 10, page: int = 1,
                                log: bool = True, **kwargs) -> dict:
        """
        Search films by a selected category and release year range.

        The result is returned in a paginated format.

        Args:
            dict_category: Category info dict containing:
                -- category_id (int)
                -- category_name (str)
            year_from: Start year (inclusive).
            year_to: End year (inclusive).
            page_size: Number of items per page.
            page: Page number (1-based).
            log: If True, writes the search query to analytics logs (only for the first request).

        Returns:
            dict: Paginated response with the following keys:
                - items (list[dict]): list of films, each item contains:
                    -- film_id (int)
                    -- title (str)
                    -- release_year (int)
                    -- category (str)
                - total (int): total matching films
                - page (int): current page number
                - page_size (int): number of items per page
                - pages (int): total number of pages
        """

        conn = get_mysql_connection()

        offset = (page - 1) * page_size
        category_id = dict_category.get("category_id")
        category_name = dict_category.get("category_name")
        try:

            period = repo.get_year_range_by_category(conn, category_id)
            allowed_from = int(period.get("year_from", 0))
            allowed_to = int(period.get("year_to", 0))

            norm_year_from, norm_year_to = normalize_year_range_for_category(
                year_from, year_to, allowed_from, allowed_to
            )

            items = repo.search_films_by_category_in_year_range(conn, category_id,
                                                                norm_year_from, norm_year_to,
                                                                page_size, offset)
            total = repo.count_films_by_category_in_year_range(conn, category_id,
                                                               norm_year_from, norm_year_to)
            pages = calculate_total_pages(total, page_size)

            years_range = f"{year_from} - {year_to}"

            if log:
                search_type = "category_year"
                params = {"category_name": category_name,
                          "years_range": years_range,
                          "results_count": total}
                log_search_query(search_type, params)

            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "pages": pages
            }
        finally:
            conn.close()

    def get_year_range_by_category(self, dict_category: dict) -> list[dict]:
        """
        Get the available release year range for a selected category.

        This method returns the minimum and maximum release years of films
        within the given category.

        Args:
            dict_category: Category info dict containing:
                - category_id (int)
                - category_name (str)

        Returns:
            dict: Year range info with the following keys:
                - year_from (int): minimum release year in the selected category
                - year_to (int): maximum release year in the selected category
                - category (str): category name
        """
        conn = get_mysql_connection()
        category_id = dict_category.get("category_id")
        try:
            items = repo.get_year_range_by_category(conn, category_id)
            return items
        finally:
            conn.close()

    def list_all_categories(self):
        """
        Get the full list of available film categories.

        This method returns all categories without pagination.

        Returns:
            list[dict]: List of categories, each item contains:
                - category_id (int)
                - category_name (str)
        """

        conn = get_mysql_connection()
        try:
            return repo.list_categories(conn)
        finally:
            conn.close()

    def get_dict_category_by_name(self, category_name):
        conn = get_mysql_connection()
        try:
            dict_category = repo.get_category_by_category_name(conn, category_name)
            return dict_category
        finally:
            conn.close()


class QueryLogService:
    def get_top_queries(self, limit: int = 5) -> list[dict]:
        """
        Get the most frequent search queries from MongoDB logs.

        This method builds an aggregated report based on logged search records and returns
        a list of formatted report rows.

        Args:
            limit: Maximum number of top queries to return (default: 5).

        Returns:
            list[dict]: List of report rows, each item contains:
                - idx (str): row number (1-based)
                - type (str): search type (e.g., "keyword", "category", "category_year")
                - query (str): human-readable query text (built from stored params)
                - count (int): how many times this query was executed
                - results (int): total results count for the query (as stored in logs)
        """

        db = get_mongo_db()
        collection = db.get_collection(name_log_collection)
        result = collection.aggregate(repo_mogo.build_top_queries_pipeline(limit))

        res = list()
        for i, item in enumerate(result, 1):
            format_dict = defaultdict(str)
            q_type = item.get('search_type')
            format_dict["idx"] = str(i)
            format_dict["type"] = q_type

            text_query = get_text_query(item)
            format_dict["query"] = text_query

            format_dict["count"] = item.get('count_query')
            format_dict["results"] = item.get('results_count')
            res.append(dict(format_dict))

        return res

    def get_last_unique_queries(self, limit: int = 5) -> list[dict]:
        """
        Get the most recent unique search queries from MongoDB logs.

        This method reads recent log records (sorted by timestamp descending) and returns
        a list of distinct queries (based on the formatted query text). The search is limited
        to a recent window (up to 200 latest records) to keep processing fast.

        Args:
            limit: Maximum number of unique queries to return (default: 5).

        Returns:
            list[dict]: List of report rows, each item contains:
                - idx (str): row number (1-based)
                - type (str): search type (e.g., "keyword", "category", "category_year")
                - query (str): human-readable query text (built from stored params)
                - timestamp (str): formatted timestamp of the latest occurrence
                - results (int): total results count for the query (as stored in logs)
        """
        db = get_mongo_db()
        collection = db.get_collection(name_log_collection)
        result = collection.aggregate(repo_mogo.build_last_unique_queries_pipeline())

        unique_queries = []
        res = list()
        idx = 0
        for i, item in enumerate(result, 1):
            format_dict = defaultdict(str)
            q_type = item.get('search_type')

            format_dict["type"] = q_type

            text_query = get_text_query(item)

            format_dict["query"] = text_query

            format_date = get_format_date(item.get('timestamp'))
            format_dict["timestamp"] = format_date
            format_dict["results"] = item.get('results_count')

            if text_query not in unique_queries:
                unique_queries.append(text_query)
                idx += 1
                format_dict["idx"] = str(i)
                res.append(dict(format_dict))

            if idx >= limit:
                break

        return res


def log_search_query(search_type: str, params: dict) -> None:
    """
    Write a search query log record to MongoDB.

    This function stores analytics data about search requests, including timestamp,
    search type, and search parameters.

    Args:
        search_type: Search action type (e.g., "keyword", "category_name", "category_year").
        params: Dictionary with search parameters and additional info (e.g., keyword/category,
            year range, results count).
    """
    rec = dict()
    rec["timestamp"] = datetime.now().isoformat()
    rec["search_type"] = search_type
    rec["params"] = params
    try:
        db = get_mongo_db()
        collection = db.get_collection(name_log_collection)
        collection.insert_one(rec)

    except PyMongoError as err:
        # raise MongoLoggingError("Failed to write query log to MongoDB") from err
        pass


if __name__ == '__main__':
    search = FilmSearchService()
    print('get_dict_category_by_name', search.get_dict_category_by_name("Action"))
    # keyword = 'matrix'
    # print('keyword', keyword, search.search_by_keyword(keyword, log=False))
    # category = {"category_id": 1, "category_name": "Action"}
    # print('category', category.get("category_name"), search.search_by_category(category, log=False))
    # # category = 500
    # print('year_range_by_category_id', category.get("category_name"), search.get_year_range_by_category(category))
    # year_from = 1999
    # year_to = 2000
    # print('category_year', category, search.search_by_category_year(category, year_from, year_to, log=False))
