from pymongo import MongoClient
from app.core.db.local_settings import MONGODB_URL_WRITE

_client = None


def get_mongo_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URL_WRITE)
    return _client


def get_mongo_db():
    client = get_mongo_client()
    db_name = "ich_edit"
    # collection_name = "final_project_010825_albert"
    return client[db_name]


if __name__ == '__main__':
    get_mongo_db()
