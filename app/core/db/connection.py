#  pip install mysql-connector-python
from app.core.exceptions import DatabaseConnectionError
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool

from app.core.db.local_settings import dbconfig

_pool = None


def create_mysql_connection():
    """
    Create a new direct MySQL connection.

    This function connects to the MySQL database using the configuration from
    local settings.

    Returns:
        MySQLConnection: Active MySQL connection.

    Raises:
        DatabaseConnectionError: If the connection to MySQL cannot be established.
    """
    try:
        connection = mysql.connector.connect(**dbconfig)
        return connection
    except mysql.connector.Error as err:
        raise DatabaseConnectionError("Failed to connect to MySQL") from err


def get_mysql_pool() -> MySQLConnectionPool:
    """
    Get (or create) a global MySQL connection pool.

    The pool is created only once and then reused for the whole application
    runtime.

    Returns:
        MySQLConnectionPool: MySQL connection pool instance.

    Raises:
        DatabaseConnectionError: If the pool cannot be created.
    """
    global _pool
    if _pool is None:
        try:
            _pool = MySQLConnectionPool(
                pool_name="search_film_pool",
                pool_size=20,
                **dbconfig
            )
        except mysql.connector.Error as err:
            raise DatabaseConnectionError("Failed to create MySQL connection pool") from err
    return _pool


def get_mysql_connection():
    """
    Get a MySQL connection from the global connection pool.

    Returns:
        MySQLConnection: A connection instance from the pool.

    Raises:
        DatabaseConnectionError: If a connection cannot be obtained from the pool.
    """
    try:
        pool = get_mysql_pool()
        return pool.get_connection()
    except mysql.connector.Error as err:
        raise DatabaseConnectionError("Failed to get MySQL connection from pool") from err
    # return create_mysql_connection()


if __name__ == '__main__':
    print('get_mysql_connection()', get_mysql_connection())
