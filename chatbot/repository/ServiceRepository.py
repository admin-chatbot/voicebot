# repository/ServiceRepository.py
from pymongo import MongoClient
from pymongo.server_api import ServerApi

class ServiceRepository:
    def __init__(self, db_type, uri, username="", password=""):
        print("uri is ",uri)
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client.get_database("command_center")

    def find_by_keyword(self, keyword_field, keyword_value,client_id):
        # Your query logic here
        # For example, using the 'products' collection:
        collection = self.db.service
        query = {keyword_field: keyword_value,"clientId":client_id}
        print(f"query is '{query}'")
        results = collection.find(query)
        return results
    
    def query_service_params(self,serviceId):
        collection = self.db.serviceparameters
        query = {"serviceId":serviceId}
        results = collection.find(query)
        print(f"service parameters results are:- '{results}'")
        return results
    
    def insert_data_to_servicelog(self, keyword_field, keyword_value, client_id,endpoint):
        # Your insertion logic here
        # For example, using the 'service' collection:
        collection = self.db.servicelog
        document = {keyword_field: keyword_value, "client": client_id,"endpoint":endpoint}
        result = collection.insert_one(document)
        return result.inserted_id
    
    def insert_data_to_botrequestlog(self, data):
        # Your insertion logic here
        # For example, using the 'service' collection:
        collection = self.db.botrequestlog
        document = data
        result = collection.insert_one(document)
        return result.inserted_id
    
    def get_next_sequence_value(self,sequence_name):
        self.collection = self.db.database_sequences
        self.sequence_name = sequence_name
        sequence_doc = self.collection.find_one_and_update(
            {'_id': self.sequence_name},
            {'$inc': {'sequence_value': 1}},
            upsert=True,
            return_document=True
        )
        return sequence_doc['sequence_value']
    
    def update_user_action(self,document,query):
        collection = self.db.user_actions
        result = collection.update_one(query, {"$set": document})
        return result
    
    def query_user_action(self,user_id):
        collection = self.db.user_actions
        query = {"user_id":user_id}
        results = collection.find(query)
        if results:
            for result in results:
                print("user action found found:", result)
                return result
            else:
                print("No documents found for user:", user_id)
                return None

    def delete_user_action(self,user_id):
        collection = self.db.user_actions
        query = {"user_id":user_id}
        results = collection.find_one_and_delete(query)
        if results:
            for result in results:
                print("user action found found:", result)
                return result
            else:
                print("No documents found for user:", user_id)
                return None
    
    def create_user_action(self,document):
        collection = self.db.user_actions
        results = collection.insert_one(document)
        return collection.find_one(results.inserted_id)
    
    def close_connection(self):
        self.client.close()
