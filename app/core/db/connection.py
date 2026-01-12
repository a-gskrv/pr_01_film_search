#  pip install mysql-connector-python

import mysql.connector
from local_settings import dbconfig

class DatabaseConnectionError(RuntimeError):
    pass

def get_mysql_connection():
    try:
        connection = mysql.connector.connect(**dbconfig)
        return connection
    except mysql.connector.Error as err:
        raise DatabaseConnectionError("Failed to connect to MySQL") from err


if __name__ == '__main__':
    print(get_mysql_connection())
