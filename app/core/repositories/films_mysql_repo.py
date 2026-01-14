LIST_CATEGORIES_SQL = """
SELECT 
    category_id,
    name
FROM category
;
"""

SEARCH_FILMS_BY_TITLE_LIKE_SQL = """
SELECT 
    film_id,
    title,
    release_year
FROM film
WHERE LOWER(title) LIKE LOWER(%(keyword)s)
LIMIT %(limit)s
OFFSET %(offset)s
;
"""

COUNT_FILMS_BY_TITLE_LIKE_SQL = """
SELECT COUNT(*) AS total
FROM film
WHERE LOWER(title) LIKE LOWER(%(keyword)s)
;
"""

SEARCH_FILMS_BY_CATEGORY_SQL = """
SELECT 
    f.film_id, f.title, f.release_year, c.name
FROM
    film AS f
        JOIN
    film_category AS fc ON (f.film_id = fc.film_id)
        JOIN
    category AS c ON (fc.category_id = c.category_id)
WHERE
    c.category_id = %(category_id)s
LIMIT %(limit)s
OFFSET %(offset)s
;
"""

COUNT_FILMS_BY_CATEGORY_SQL = """
SELECT COUNT(DISTINCT f.film_id) AS total
FROM
    film AS f
        JOIN
    film_category AS fc ON (f.film_id = fc.film_id)
        JOIN
    category AS c ON (fc.category_id = c.category_id)
WHERE
    c.category_id = %(category_id)s
;
"""

SEARCH_FILMS_BY_CATEGORY_IN_YEAR_RANGE_SQL = """
SELECT 
    f.film_id, f.title, f.release_year, c.name
FROM
    film AS f
        JOIN
    film_category AS fc ON (f.film_id = fc.film_id)
        JOIN
    category AS c ON (fc.category_id = c.category_id)
WHERE
    c.category_id = %(category_id)s AND f.release_year BETWEEN %(year_from)s AND %(year_to)s
LIMIT %(limit)s
OFFSET %(offset)s
;
"""

COUNT_FILMS_BY_CATEGORY_IN_YEAR_RANGE_SQL = """
SELECT COUNT(DISTINCT f.film_id) AS total
FROM
    film AS f
        JOIN
    film_category AS fc ON (f.film_id = fc.film_id)
        JOIN
    category AS c ON (fc.category_id = c.category_id)
WHERE
    c.category_id = %(category_id)s AND f.release_year BETWEEN %(year_from)s AND %(year_to)s
;
"""

GET_YEAR_RANGE_BY_CATEGORY_ID_SQL = """
SELECT  
MIN(f.release_year) as year_from,
MAX(f.release_year) as year_to,
c.name
FROM
    film AS f
        JOIN
    film_category AS fc ON (f.film_id = fc.film_id)
        JOIN
    category AS c ON (fc.category_id = c.category_id)
WHERE
    c.category_id = %(category_id)s
GROUP BY c.category_id
;
"""


def list_categories(conn) -> list[dict]:
    with conn.cursor(dictionary=True) as cursor:
        # parameters = {"limit": limit, "offset": offset}
        cursor.execute(LIST_CATEGORIES_SQL)
        items = cursor.fetchall()

        return items


def get_year_range_by_category_id(conn, category_id) -> list[dict]:
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"category_id": category_id}
        cursor.execute(GET_YEAR_RANGE_BY_CATEGORY_ID_SQL, parameters)
        items = cursor.fetchone()

    return items


def search_films_by_title_like(conn, keyword: str, limit: int = 10, offset: int = 0) -> list[dict]:
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"keyword": f"%{keyword}%", "limit": limit, "offset": offset}
        cursor.execute(SEARCH_FILMS_BY_TITLE_LIKE_SQL, parameters)
        items = cursor.fetchall()
    return items


def count_films_by_title_like(conn, keyword: str) -> int:
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"keyword": f"%{keyword}%"}
        cursor.execute(COUNT_FILMS_BY_TITLE_LIKE_SQL, parameters)
        row = cursor.fetchone()

    return int(row["total"] if row else 0)


def search_films_by_category(conn, category_id: str, limit: int = 10, offset: int = 0) -> list[dict]:
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"category_id": category_id, "limit": limit, "offset": offset}
        cursor.execute(SEARCH_FILMS_BY_CATEGORY_SQL, parameters)
        items = cursor.fetchall()

    return items


def count_films_by_category(conn, category_id: str) -> int:
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"category_id": category_id}
        cursor.execute(COUNT_FILMS_BY_CATEGORY_SQL, parameters)
        row = cursor.fetchone()

    return int(row["total"] if row else 0)


def search_films_by_category_in_year_range(conn, category_id: str, year_from: int, year_to: int, limit: int = 10,
                                           offset: int = 0) -> list[dict]:
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"category_id": category_id, "year_from": year_from, "year_to": year_to, "limit": limit,
                      "offset": offset}
        cursor.execute(SEARCH_FILMS_BY_CATEGORY_IN_YEAR_RANGE_SQL, parameters)
        items = cursor.fetchall()

    return items


def count_films_by_category_in_year_range(conn, category_id: str, year_from: int, year_to: int) -> int:
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"category_id": category_id, "year_from": year_from, "year_to": year_to}
        cursor.execute(COUNT_FILMS_BY_CATEGORY_IN_YEAR_RANGE_SQL, parameters)
        row = cursor.fetchone()

    return int(row["total"] if row else 0)


if __name__ == '__main__':
    pass
