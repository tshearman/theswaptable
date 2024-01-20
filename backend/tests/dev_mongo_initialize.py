import pymongo

from resources.sample_data import items, users


def setup(client: pymongo.MongoClient):
    db_name = "theswaptable_dev"
    db = client[db_name]
    item_collection = db["items"]
    user_collection = db["users"]
    item_dicts = [i.dict() for i in items]
    item_collection.insert_many(item_dicts)
    user_collection.insert_many([u.dict() for u in users])


def teardown(client: pymongo.MongoClient):
    db_name = "theswaptable_dev"
    db = client[db_name]
    item_collection = db["items"]
    user_collection = db["users"]
    item_collection.delete_many({})
    user_collection.delete_many({})


if __name__ == "__main__":
    user = "root"
    pw = "example"
    client = pymongo.MongoClient(f"mongodb://{user}:{pw}@mongo:27017/")
    setup(client)
