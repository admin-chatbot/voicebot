# utilities.py

import json
import subprocess


# Function to make a curl request and parse the JSON response
def get_stock_data(symbol):
    curl_command = f'curl "https://finnhub.io/api/v1/quote?symbol={symbol}&token=cll916pr01qhqdq2qjqgcll916pr01qhqdq2qjr0"'
    response = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    return json.loads(response.stdout)

# Function to generate a bot response for stock-related intent
def generate_stock_response(entities, stock_data):
    c_property_value = stock_data.get("c")
    return f"Current share price of {entities} is - {c_property_value}"

def get_user_id_from_cookie(request):
    user_id_cookie = request.cookies.get('userId')
    print("request for user-", user_id_cookie)
    if user_id_cookie:
        return user_id_cookie
    else:
        return ''

def generate_mongo_response(results):
    print(f"mongo response '{results}'")
    response = get_services_data(results[0]['endpoint'])
    return f"response found from mongoDB is - {response}"

def get_services_data(url):
    print(f"calling endpoint '{url}'")
    curl_command = f'curl "{url}"'
    response = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    return json.loads(response.stdout)

