# utilities.py

import json
import subprocess
import requests
from flask import request, Response
from middleware.InitiateMiddleware import query_service_parameters

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

def generate_mongo_response(results,intent):
    endpoint = results[0]['endpoint']
    method = results[0]['method']
    response_schema = results[0]['responseSchema']
    bot_response_template = results[0]['botResponseTemplate']  
    serviceId = results[0]['_id']
    params = get_services_params_data(serviceId) 
    response = make_request(endpoint, method,params)
    if response == "request_parameter":
        return {"requestParameter":params[0]['name'],"description":params[0]['description'],"intent":intent}
    print(f"mongo response '{results}'")
    response = parse_response(response, response_schema, bot_response_template)
    return f"{response}"

def get_services_params_data(serviceId):
    print(f"getting service parameters for '{serviceId}'")
    results = query_service_parameters(serviceId)
    service_params = []
    print(f"Total results '{results}'")
    for product in results:
        print(product)
        value = product.get("name")  # Replace "value" with the actual field name
        service_params.append(product)
        print(value)
    print(f"service parameter data is :-'{service_params}'")

    return service_params

def parse_response(response, response_schema, bot_response_template):
    if response is None:
        return None
    
    processed_response = bot_response_template
    for key, value in response.items():
        if key in processed_response:
            split_keys = key.split('.')
            result = response
            for key in split_keys:
                result = result[key]
            processed_response = processed_response.replace('{{' + key + '}}', result)
    
    return processed_response

def make_request(endpoint, method,params):
    if params:
        if params[0]['type'] == "query_param":
            query_param = params[0]['name']
            query_param_value = request.cookies.get(query_param)
            if query_param_value:
                endpoint = endpoint.replace(f"{{{{{query_param}}}}}", query_param_value)
            else:
                return "request_parameter"
        elif params[0]['type'] == "path_param":
            path_param = params[0]['name']
            path_param_value = request.cookies.get(params[0]['path_param'])
            if path_param_value:
                endpoint = endpoint.replace(f"{{{{{path_param}}}}}", path_param_value)
            else:
                return "request_parameter"
        elif params[0]['type'] == "body":
            body = params[0]['name']
            body_value = request.cookies.get(body)
            if body_value:
                endpoint = endpoint.replace(f"{{{{{body}}}}}", body_value)
            else:
                return "request_parameter"
    else:
        print("params_array_empty")

    if method == 'GET':
        response = requests.get(endpoint)
        return response.json() if response.status_code == 200 else None
    # Add handling for other HTTP methods if needed
    if method == 'POST':
        response = requests.post(endpoint,params)
        return response.json() if response.status_code == 200 else None
    # Add handling for other HTTP methods if needed
def extract_query_params(params):
    if params and params[0].query_params:
        query_param = params[0].query_params[0]
    else:
        query_param = None

    if params and params.body:
        body_param = params.body
    else:
        body_param = None

    if params and params[0].path_params:
        path_param = params[0].path_params
    else:
        path_param = None

    