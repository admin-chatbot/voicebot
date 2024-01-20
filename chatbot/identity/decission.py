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
            return 'Unknown Client ID'
    else:
        return 'clientID'
