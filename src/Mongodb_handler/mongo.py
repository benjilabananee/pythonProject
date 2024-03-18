from pymongo import MongoClient, UpdateOne


class MongoDBManager:
    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]

    def insert_document(self, collection_name, document: dict):
        try:
            collection = self.db[collection_name]
            collection.insert_one(document)
        except Exception as e:
            print(f"Error inserting document into {collection_name}: {e}")

    def update_document(self, key, value_to_search, replacement_value, collection_name):
        try:
            collection = self.db[collection_name]
            query = {key: value_to_search}
            update_query = {'$set': replacement_value}
            collection.update_one(query, update_query)
        except Exception as e:
            print(f"Error updating document in {collection_name}: {e}")

    def find_document_by_key(self, key, value_to_search, collection_name):
        try:
            collection = self.db[collection_name]
            existing_document = collection.find_one({key: value_to_search})
            return existing_document
        except Exception as e:
            print(f"Error finding document by key in {collection_name}: {e}")
            return None

    def find_document_by_dynamic_key(self, key, collection_name):
        try:
            collection = self.db[collection_name]
            existing_document = collection.find_one({key: {'$exists': True}})
            return existing_document
        except Exception as e:
            print(f"Error finding document by dynamic key in {collection_name}: {e}")
            return None

    def close_connection(self):
        try:
            self.client.close()
            print("MongoDB connection closed.")
        except Exception as e:
            print(f"Error closing MongoDB connection: {e}")