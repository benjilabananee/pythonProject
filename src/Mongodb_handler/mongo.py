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

    def update_document(self, key, value_to_search, replacement_value, collection_name):
        collection = self.db[collection_name]
        query = {key: value_to_search}
        update_query = {'$set': replacement_value}
        print(value_to_search)
        collection.update_one(query, update_query)

    def find_document_by_key(self, key, value_to_search, collection_name):
        collection = self.db[collection_name]
        existing_document = collection.find_one({key: value_to_search})
        return existing_document

    def find_document_by_dynamic_key(self, key, collection_name):
        collection = self.db[collection_name]
        existing_document = collection.find_one({key: {'$exists': True}})
        return existing_document


