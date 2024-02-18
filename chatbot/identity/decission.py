import json
def decision_module(request):
    # Extract the client ID from the request cookies
    client_id_cookie = request.cookies.get('client_id')

    # Check for null (None) or empty string
    if client_id_cookie is not None and client_id_cookie != '':
        # Make decisions based on the client ID
        if client_id_cookie == 'premium':
            return 'Welcome Premium User!'
        elif client_id_cookie == 'standard':
            return 'Welcome Standard User!'
        else:
            return client_id_cookie
      
    else:
        with open("client_config.json", "r") as client_config_file:
            client_config = json.load(client_config_file)
            client_id = client_config.get("client_id", 0)
            # Check if the intent is related to "stocks"
            if client_id == 0 :
                return 'clientID'
            else: 
                return client_id
