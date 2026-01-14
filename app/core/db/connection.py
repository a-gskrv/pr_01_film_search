#  pip install mysql-connector-python

import mysql.connector
from app.core.db.local_settings import dbconfig

class DatabaseConnectionError(RuntimeError):
    pass

def create_mysql_connection():
    try:
        connection = mysql.connector.connect(**dbconfig)
        return connection
    except mysql.connector.Error as err:
        raise DatabaseConnectionError("Failed to connect to MySQL") from err

def get_mysql_connection():
    return create_mysql_connection()


if __name__ == '__main__':
    print('get_mysql_connection()', get_mysql_connection())
