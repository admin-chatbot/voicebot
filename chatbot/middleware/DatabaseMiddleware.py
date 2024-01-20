# middleware/DatabaseMiddleware.py
from repository.ServiceRepository import ServiceRepository

class DatabaseMiddleware:
    def __init__(self, db_type, uri, username="", password=""):
        self.repository = ServiceRepository(db_type, uri, username, password)

    def execute_query(self, keyword_field, keyword_value,client_id):
        return self.repository.find_by_keyword(keyword_field, keyword_value, client_id)
    
    def execute_servicelog_insert(self, keyword_field, keyword_value):
        return self.repository.insert_data_to_servicelog(keyword_field, keyword_value,data={})

    def execute_botrequestlog_insert(self, document):
        return self.repository.insert_data_to_botrequestlog(data=document)

    def close_connection(self):
        self.repository.close_connection()
