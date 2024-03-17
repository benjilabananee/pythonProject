from bson import ObjectId
from pymongo import MongoClient, UpdateOne


class MongoDBManager:
    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]

    def insert_document(self, collection_name, document: dict):
        collection = self.db[collection_name]
        collection.insert_one(document)

    def update_document(self, collection_name, key, new_value):
        collection = self.db[collection_name]
        update_operation = collection.update_one({key: {'$exists': True}}, {'$set': {key: new_value}})
        print(update_operation)

    def find_document_by_key(self, collection_name, key: str):
        collection = self.db[collection_name]
        existing_document = collection.find_one({key: {'$exists': True}})
        return existing_document
