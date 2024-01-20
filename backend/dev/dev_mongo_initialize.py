import pymongo

from dev_data import items, users


def setup(client: pymongo.MongoClient):
    db_name = "theswaptable_dev"
    db = client[db_name]
    item_collection = db["items"]
    user_collection = db["users"]
    item_dicts = [i.model_dump() for i in items]
    item_collection.insert_many(item_dicts)
    user_collection.insert_many([u.model_dump() for u in users])


def teardown(client: pymongo.MongoClient):
    db_name = "theswaptable_dev"
    db = client[db_name]
    item_collection = db["items"]
    user_collection = db["users"]
    item_collection.delete_many({})
    user_collection.delete_many({})


if __name__ == "__main__":
    user = "root"
    pw = "abcd"
    port = "27017"
    client = pymongo.MongoClient(
        f"mongodb://{user}:{pw}@mongo:{port}/", uuidRepresentation="standard"
    )
    setup(client)
