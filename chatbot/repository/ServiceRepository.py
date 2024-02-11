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

    def close_connection(self):
        self.client.close()
