# utilities.py

import json
import subprocess
import spacy

# Load the English NLP model from SpaCy
nlp = spacy.load("en_core_web_sm")

# Function to extract named entities from user input using SpaCy
def extract_entities(user_input):
    doc = nlp(user_input)
    return [ent.text for ent in doc.ents if ent.label_ == "ORG"]

# Function to make a curl request and parse the JSON response
def get_stock_data(symbol):
    curl_command = f'curl "https://finnhub.io/api/v1/quote?symbol={symbol}&token=cll916pr01qhqdq2qjqgcll916pr01qhqdq2qjr0"'
    response = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    return json.loads(response.stdout)

# Function to generate a bot response for stock-related intent
def generate_stock_response(entities, stock_data):
    c_property_value = stock_data.get("c")
    return f"Current share price of {entities[0]} is - {c_property_value}"
