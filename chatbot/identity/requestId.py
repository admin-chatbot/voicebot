import uuid

def generate_request_id():
    return str(uuid.uuid4())

request_id = generate_request_id()
print("Request ID:", request_id)
