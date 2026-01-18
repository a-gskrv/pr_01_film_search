from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.core.db.local_settings import MONGODB_URL_WRITE

from app.core.exceptions import MongoConnectionError

_client = None


def get_mongo_client() -> MongoClient:
    """
    Get (or create) a global MongoDB client.

    The MongoClient instance is created only once and then reused for the whole
    application runtime (MongoClient manages its own internal connection pool).

    Returns:
        MongoClient: MongoDB client instance.

    Raises:
        MongoConnectionError: If the MongoDB client cannot be created.
    """
    global _client
    if _client is None:
        try:
            _client = MongoClient(MONGODB_URL_WRITE)
        except PyMongoError as err:
            raise MongoConnectionError("Failed to create MongoDB client") from err
    return _client


def get_mongo_db():
    """
    Get the MongoDB database used for query logging and reports.

    Returns:
        Database: MongoDB database instance.

    Raises:
        MongoConnectionError: If MongoDB connection fails.
    """
    try:
        db = get_mongo_client()
        client = get_mongo_client()
        db_name = "ich_edit"
        return client[db_name]
    except PyMongoError  as err:
        raise MongoConnectionError("Failed to get MongoDB database") from err


if __name__ == '__main__':
    get_mongo_db()
