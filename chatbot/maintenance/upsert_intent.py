from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Function to load JSON data from file
def load_data():
    with open('chatbot/intents.json', 'r') as file:
        data = json.load(file)
    return data

# Function to save JSON data to file
def save_data(data):
    with open('chatbot/intents.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/insert_or_modify', methods=['POST'])
def insert_or_modify_record():
    try:
        data = load_data()
        request_data = request.json  # Assuming the request contains JSON data

        # Check if the request contains all required fields
        if 'intent' not in request_data or 'context' not in request_data or 'patterns' not in request_data or 'responses' not in request_data:
            return jsonify({'error': 'Incomplete data. Required fields: intent, context, patterns, responses'}), 400

        # Check if the intent already exists
        intent_exists = False
        for intent in data['intents']:
            if intent['tag'] == request_data['intent']:
                intent_exists = True
                # Modify existing record
                intent['context'] = request_data['context']
                intent['patterns'] = request_data['patterns']
                intent['responses'] = request_data['responses']
                break
        
        # If intent doesn't exist, insert new record
        if not intent_exists:
            new_intent = {
                'context': request_data['context'],
                'patterns': request_data['patterns'],
                'responses': request_data['responses'],
                'tag': request_data['intent']
            }
            data['intents'].append(new_intent)

        # Save the modified data back to the file
        save_data(data)

        return jsonify({'message': 'Record inserted/modified successfully'}), 200

    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
