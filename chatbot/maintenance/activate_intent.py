import json


# Function to load JSON data from file
def load_data():
    with open('intent_config.json', 'r') as file:
        data = json.load(file)
    return data

# Function to save JSON data to file
def save_data(data):
    with open('intent_config.json', 'w') as file:
        json.dump(data, file, indent=4)

def activate_intent(data):
    try:
        data = load_data()
        request_data = data  # Assuming the request contains JSON data

        # Check if the request contains the 'intent_name'
        if 'intent_name' not in request_data:
            return {'error': 'Missing intent_name in request'}

        intent_name = request_data['intent_name']
        if intent_name in data['intentList']:
            return {'message': f'Intent {intent_name} activated successfully'}
        else:
            return {'error': f'Intent {intent_name} not found'}

    except FileNotFoundError:
        return  {'error': 'File not found'}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True)
