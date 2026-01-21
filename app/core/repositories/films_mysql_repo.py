LIST_CATEGORIES_SQL = """
SELECT 
    category_id,
    name AS category_name
FROM category
;
"""

GET_CATEGORIES_BY_NAME_SQL = """
SELECT 
    category_id,
    name AS category_name
FROM category
WHERE
    LOWER(name) = LOWER(%(category_name)s)
;
"""

SEARCH_FILMS_BY_TITLE_LIKE_SQL = """
SELECT 
    f.film_id,
    f.title,
    f.release_year,
    c.name AS category_name
FROM
    film AS f
        JOIN
    film_category AS fc ON (f.film_id = fc.film_id)
        JOIN
    category AS c ON (fc.category_id = c.category_id)
WHERE LOWER(f.title) LIKE LOWER(%(keyword)s)
LIMIT %(limit)s
OFFSET %(offset)s
;
"""

COUNT_FILMS_BY_TITLE_LIKE_SQL = """
SELECT COUNT(DISTINCT f.film_id) AS total
FROM
    film AS f
        JOIN
    film_category AS fc ON (f.film_id = fc.film_id)
        JOIN
    category AS c ON (fc.category_id = c.category_id)
WHERE LOWER(f.title) LIKE LOWER(%(keyword)s)
;
"""

SEARCH_FILMS_BY_CATEGORY_SQL = """
SELECT 
    f.film_id AS film_id, f.title AS title, f.release_year AS release_year, c.name AS category_name
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
    f.film_id AS film_id, f.title AS title, f.release_year AS release_year, c.name AS category_name
FROM
    film AS f
        JOIN
    film_category AS fc ON (f.film_id = fc.film_id)
        JOIN
    category AS c ON (fc.category_id = c.category_id)
WHERE
    c.category_id = %(category_id)s AND CAST(f.release_year AS UNSIGNED) BETWEEN %(year_from)s AND %(year_to)s
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
c.name AS category_name
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
    """
        Get the full list of film categories.

        Args:
            conn: Active MySQL connection.

        Returns:
            list[dict]: List of categories, each item contains:
                - category_id (int)
                - category_name (str)
        """
    with conn.cursor(dictionary=True) as cursor:
        # parameters = {"limit": limit, "offset": offset}
        cursor.execute(LIST_CATEGORIES_SQL)
        items = cursor.fetchall()

        return items


def get_category_by_category_name(conn, category_name) -> dict:
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"category_name": category_name}
        cursor.execute(GET_CATEGORIES_BY_NAME_SQL, parameters)
        items = cursor.fetchone()
    return items



def get_year_range_by_category(conn, category_id: str) -> list[dict]:
    """
    Get the available release year range for a selected category.

    Args:
        conn: Active MySQL connection:
        category_id: Category ID.

    Returns:
        dict: Year range info with the following keys:
            - year_from (int)
            - year_to (int)
            - category (str)
    """

    with conn.cursor(dictionary=True) as cursor:
        parameters = {"category_id": category_id}
        cursor.execute(GET_YEAR_RANGE_BY_CATEGORY_ID_SQL, parameters)
        items = cursor.fetchone()

    return items


def search_films_by_title_like(conn, keyword: str, limit: int = 10, offset: int = 0) -> list[dict]:
    """
    Search films by a keyword in the film title.

    Args:
        conn: Active MySQL connection.
        keyword: Keyword to search for.
        limit: Maximum number of results to return.
        offset: Number of items to skip (for pagination).

    Returns:
        list[dict]: List of films, each item contains:
            - film_id (int)
            - title (str)
            - release_year (int)
    """
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"keyword": f"%{keyword}%", "limit": limit, "offset": offset}
        cursor.execute(SEARCH_FILMS_BY_TITLE_LIKE_SQL, parameters)
        items = cursor.fetchall()
    return items


def count_films_by_title_like(conn, keyword: str) -> int:
    """
    Count films matching a keyword in the film title.

    Args:
        conn: Active MySQL connection.
        keyword: Keyword to search for.

    Returns:
        int: Total number of matching films.
    """
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"keyword": f"%{keyword}%"}
        cursor.execute(COUNT_FILMS_BY_TITLE_LIKE_SQL, parameters)
        row = cursor.fetchone()

    return int(row["total"] if row else 0)


def search_films_by_category(conn, category_id: str, limit: int = 10, offset: int = 0) -> list[dict]:
    """
    Search films by category.

    Args:
        conn: Active MySQL connection.
        category_id: Category ID.
        limit: Maximum number of results to return.
        offset: Number of items to skip (for pagination).

    Returns:
        list[dict]: List of films, each item contains:
            - film_id (int)
            - title (str)
            - release_year (int)
            - category (str)
    """
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"category_id": category_id, "limit": limit, "offset": offset}
        cursor.execute(SEARCH_FILMS_BY_CATEGORY_SQL, parameters)
        items = cursor.fetchall()

    return items


def count_films_by_category(conn, category_id: str) -> int:
    """
    Count films in the selected category.

    Args:
        conn: Active MySQL connection.
        category_id: Category ID.

    Returns:
        int: Total number of matching films.
    """
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"category_id": category_id}
        cursor.execute(COUNT_FILMS_BY_CATEGORY_SQL, parameters)
        row = cursor.fetchone()

    return int(row["total"] if row else 0)


def search_films_by_category_in_year_range(conn, category_id: str,
                                           year_from: int, year_to: int,
                                           limit: int = 10, offset: int = 0) -> list[dict]:
    """
        Search films by category and release year range.

        Args:
            conn: Active MySQL connection.
            category_id: Category ID.
            year_from: Start year (inclusive).
            year_to: End year (inclusive).
            limit: Maximum number of results to return.
            offset: Number of items to skip (for pagination).

        Return:
            list[dict]: List of films, each item contains:
                - film_id (int)
                - title (str)
                - release_year (int)
                - category (str)
        """

    with conn.cursor(dictionary=True) as cursor:
        parameters = {"category_id": category_id, "year_from": year_from, "year_to": year_to, "limit": limit,
                      "offset": offset}
        cursor.execute(SEARCH_FILMS_BY_CATEGORY_IN_YEAR_RANGE_SQL, parameters)
        items = cursor.fetchall()

    return items


def count_films_by_category_in_year_range(conn, category_id: str, year_from: int, year_to: int) -> int:
    """
    Count films in the selected category within the given year range.

        Args:
            conn: Active MySQL connection.
            category_id: Category ID.
            year_from: Start year (inclusive).
            year_to: End year (inclusive).

        Returns:
            int: Total number of matching films.
    """
    with conn.cursor(dictionary=True) as cursor:
        parameters = {"category_id": category_id, "year_from": year_from, "year_to": year_to}
        cursor.execute(COUNT_FILMS_BY_CATEGORY_IN_YEAR_RANGE_SQL, parameters)
        row = cursor.fetchone()

    return int(row["total"] if row else 0)


if __name__ == '__main__':
    pass
