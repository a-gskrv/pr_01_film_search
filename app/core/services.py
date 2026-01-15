from app.core.db.connection import get_mysql_connection
from app.core.repositories import films_mysql_repo as repo


def calculate_total_pages(total: int, page_size: int) -> int:
    if total > 0:
        pages = (total + page_size - 1) // page_size
    else:
        pages = 0
    return pages


class FilmSearchService:

    def search_by_keyword(self, keyword, page_size: int = 10, page: int = 1, **kwargs):
        conn = get_mysql_connection()

        offset = (page - 1) * page_size
        try:
            items = repo.search_films_by_title_like(conn, keyword, page_size, offset)
            total = repo.count_films_by_title_like(conn, keyword)
            pages = calculate_total_pages(total, page_size)

            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "pages": pages
            }
        finally:
            conn.close()

    def search_by_category(self, category, page_size: int = 10, page: int = 1, **kwargs):
        conn = get_mysql_connection()

        offset = (page - 1) * page_size
        try:
            items = repo.search_films_by_category(conn, category, page_size, offset)
            total = repo.count_films_by_category(conn, category)
            pages = calculate_total_pages(total, page_size)

            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "pages": pages
            }
        finally:
            conn.close()

    def search_by_category_year(self, category, year_from, year_to, page_size: int = 10, page: int = 1, **kwargs):
        conn = get_mysql_connection()

        offset = (page - 1) * page_size
        try:
            items = repo.search_films_by_category_in_year_range(conn, category, year_from, year_to, page_size, offset)
            total = repo.count_films_by_category_in_year_range(conn, category, year_from, year_to)
            pages = calculate_total_pages(total, page_size)

            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "pages": pages
            }
        finally:
            conn.close()

    def get_year_range_by_category_id(self, category_id) -> dict:
        conn = get_mysql_connection()
        try:
            items = repo.get_year_range_by_category_id(conn, category_id)
            return items
        finally:
            conn.close()

    def list_all_categories(self):
        conn = get_mysql_connection()
        try:
            return repo.list_categories(conn)
        finally:
            conn.close()


if __name__ == '__main__':
    search = FilmSearchService()
    keyword = 'matrix'
    print('keyword', keyword, search.search_by_keyword(keyword))
    category = 1
    print('category', category, search.search_by_category(category))
    # category = 500
    print('year_range_by_category_id', category, search.get_year_range_by_category_id(category))
    year_from = 1999
    year_to = 2000
    print('category_year', category, search.search_by_category_year(category, year_from, year_to))
