import pymongo
import json

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Select the database
db = client["mydatabase"]

# Select the collection
collection = db["mycollection"]

# Open the file containing the records
with open("records.json") as file:
    data = json.load(file)

# Insert each record into the collection
for record in data:
    insert_result = collection.insert_one(record)
    print("Inserted document ID:", insert_result.inserted_id)
