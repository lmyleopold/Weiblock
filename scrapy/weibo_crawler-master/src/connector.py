from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import pprint

MONGO_HOST = "172.17.0.2"
MONGO_PORT = 27017
MONGO_DB = "weibodata-gunshot"

c = MongoClient(MONGO_HOST, MONGO_PORT)
db = c[MONGO_DB]
collection_weibo = db["weibo"]
collection_user = db["user"]


def save(collection: str, data: dict) -> None:
    try:
        db[collection].insert_one(data)
    except DuplicateKeyError:
        pass


def in_collection(collection: str, id: dict):
    return db[collection].find_one({'id': id})


def walk_collection(collection: str):
    l = list(db[collection].find())
    for doc in l:
        yield doc


if __name__ == "__main__":
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    # collection_weibo.insert_one(test_post)
    pprint.pprint(collection_weibo.find_one({"_id": 0}))
