from datetime import datetime

from app.core.db.connection import get_mysql_connection
from app.core.db.mongo_connection import get_mongo_db
from app.core.repositories import films_mysql_repo as repo

name_log_collection = "final_project_010825_albert"

def calculate_total_pages(total: int, page_size: int) -> int:
    if total > 0:
        pages = (total + page_size - 1) // page_size
    else:
        pages = 0
    return pages


class FilmSearchService:
    def __init__(self):
        # self.connection = get_mysql_connection()
        pass

    def search_by_keyword(self, keyword, page_size: int = 10, page: int = 1, log: bool = True, **kwargs):
        conn = get_mysql_connection()
        # conn = self.connection
        offset = (page - 1) * page_size
        try:
            items = repo.search_films_by_title_like(conn, keyword, page_size, offset)
            total = repo.count_films_by_title_like(conn, keyword)
            pages = calculate_total_pages(total, page_size)

            if log:
                search_type = "keyword"
                params = {"keyword": keyword, "results_count": total}
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

    def search_by_category(self, dict_category, page_size: int = 10, page: int = 1, log: bool = True, **kwargs):
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
                params = {"category": category_name, "results_count": total}
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
                                log: bool = True, **kwargs):
        conn = get_mysql_connection()

        offset = (page - 1) * page_size
        category_id = dict_category.get("category_id")
        category_name = dict_category.get("category_name")
        try:
            items = repo.search_films_by_category_in_year_range(conn, category_id, year_from, year_to, page_size,
                                                                offset)
            total = repo.count_films_by_category_in_year_range(conn, category_id, year_from, year_to)
            pages = calculate_total_pages(total, page_size)

            years_range = f"{year_from} - {year_to}"

            if log:
                search_type = "category_year"
                params = {"category": category_name,
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

    def get_year_range_by_category(self, dict_category) -> dict:
        conn = get_mysql_connection()
        try:
            items = repo.get_year_range_by_category(conn, dict_category)
            return items
        finally:
            conn.close()

    def list_all_categories(self):
        conn = get_mysql_connection()
        try:
            return repo.list_categories(conn)
        finally:
            conn.close()


class QueryLogService:
    def get_top_queries(self, limit=5):
        db = get_mongo_db()
        collection = db.get_collection(name_log_collection)
        result = collection.aggregate([
            {
                '$addFields': {
                    'params.search_type': '$search_type'
                }
            }, {
                '$group': {
                    '_id': '$params',
                    'count_query': {
                        '$sum': 1
                    }
                }
            }, {
                '$addFields': {
                    '_id.count_query': '$count_query'
                }
            }, {
                '$sort': {
                    'count_query': -1
                }
            }, {
                '$replaceRoot': {
                    'newRoot': '$_id'
                }
            }, {
                '$limit': limit
            }
        ])
        return result

    def get_last_unique_queries(self):
        db = get_mongo_db()
        collection = db.get_collection(name_log_collection)
        result = collection.aggregate([
            {
                '$addFields': {
                    'params.search_type': '$search_type',
                    'params.timestamp': '$timestamp'
                }
            }, {
                '$replaceRoot': {
                    'newRoot': '$params'
                }
            }, {
                '$sort': {
                    'timestamp': -1
                }
            }, {
                '$limit': 200
            }
        ])
        return result


def log_search_query(search_type, params):
    rec = dict()
    rec["timestamp"] = datetime.now().isoformat()
    rec["search_type"] = search_type
    rec["params"] = params
    try:
        db = get_mongo_db()
        collection = db.get_collection(name_log_collection)
        collection.insert_one(rec)

    except KeyError:
        print("No database found")

    pass


if __name__ == '__main__':
    search = FilmSearchService()
    keyword = 'matrix'
    print('keyword', keyword, search.search_by_keyword(keyword, log=False))
    category = {"category_id": 1, "category_name": "Action"}
    print('category', category.get("category_name"), search.search_by_category(category, log=False))
    # category = 500
    print('year_range_by_category_id', category.get("category_name"), search.get_year_range_by_category(category))
    year_from = 1999
    year_to = 2000
    print('category_year', category, search.search_by_category_year(category, year_from, year_to, log=False))
