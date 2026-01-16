#  pip install mysql-connector-python

import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool

from app.core.db.local_settings import dbconfig

_pool = None


class DatabaseConnectionError(RuntimeError):
    pass


def create_mysql_connection():
    try:
        connection = mysql.connector.connect(**dbconfig)
        return connection
    except mysql.connector.Error as err:
        raise DatabaseConnectionError("Failed to connect to MySQL") from err


def get_mysql_pool() -> MySQLConnectionPool:
    global _pool
    if _pool is None:
        _pool = MySQLConnectionPool(
            pool_name="search_film_pool",
            pool_size=20,
            **dbconfig
        )
    return _pool


def get_mysql_connection():
    pool = get_mysql_pool()
    return pool.get_connection()
    # return create_mysql_connection()


if __name__ == '__main__':
    print('get_mysql_connection()', get_mysql_connection())
