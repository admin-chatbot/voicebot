# Import necessary modules
from flask import Flask, render_template, request, Response, jsonify, send_file, send_from_directory
from chatbot import predict_class, get_response
from utilities import  get_stock_data, generate_stock_response, generate_mongo_response, get_user_id_from_cookie,generate_api_response
import spacy
from middleware.InitiateMiddleware import initiate_query_lookup,insert_to_botrequestlog,query_user_action,create_user_action,update_user_action
from identity.requestId import generate_request_id
import json
from identity.decission import decision_module
from maintenance import activate_intent,upsert_intent,intent_maintenance
import os
import subprocess
import signal
from model import train_chatbot_model
import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from chatbot import predict_class
import importlib
import chatbot

# Initialize the Flask app
app = Flask(__name__)

# Function to make a curl request and parse the JSON response
# (No need to move this to utilities.py since it's specific to this script)

# Define the route for the home page
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat-form')
def chatform():
    return render_template('chat-form.html')
# Define the route for handling user input and generating responses
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get user input from the form
        user_input = request.form['user_input']
        user_id = request.form['user_id']
        print("request for user-", user_id)
        result = decision_module(request)
        if result=="clientID":
            return Response("requestClientID", content_type='text/plain')
        # Process user input using the chatbot's predict_class function
        client_id=result
        processed_input = predict_class(user_input)
        # Load intent list from intent_config.json
        user_intent=None
        request_id=None
        # Check if the intent is related to "stocks"
        user_intent=processed_input[0]['intent']
        if processed_input[0]['intent'] == "stocks":
            # Extract named entities from user input
            doc = nlp(user_input)
            entities = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
            stock_data = get_stock_data()

            # Generate a bot response with stock information
            bot_response = generate_stock_response(entities, stock_data)
        
        else:
            # If the intent is not related to stocks, get a general response from the chatbot
            keyword_value = processed_input[0]['intent']

            # Call the initiatemiddleware function to retrieve data from MongoDB
            #results = initiate_query_lookup(keyword_field, keyword_value,client_id)
            # Additional processing based on the MongoDB data can be added here if needed
            # For example, you can generate a response using the retrieved data
            try:
                results = query_user_action(user_id)
                if results is None:
                    results=create_user_action(user_id,generate_request_id(),action="start")
                    request_id=results["requestId"]
                    results = initiate_query_lookup("keyword",  keyword_value,int(client_id))
                    if len(results) > 0:
                        bot_response = generate_mongo_response(results,keyword_value,user_id)
                    else:
                        bot_response = get_response(processed_input)
                
                elif results["action"] == "request_params":
                    print ("directly call the endpoint to get results")
                    request_id=results["requestId"]
                    bot_response=generate_api_response(results,user_input,user_id)

                else:
                    request_id=results["requestId"]
                    results = initiate_query_lookup("keyword",  keyword_value,int(client_id))
                    if len(results) > 0:
                        bot_response = generate_mongo_response(results,keyword_value,user_id)
                    else:
                        bot_response = get_response(processed_input)
                    
            except Exception as e:
                print ("Error fetching intents from repository")
                update_user_action(user_id,endpoint="",method="",response_schema="",bot_response_template="",serviceId="",params="",action="error")
                bot_response = get_response(processed_input)

        # Render the template with user input and bot response
        if isinstance(bot_response, dict):
            json_response = json.dumps(bot_response)
            insert_to_botrequestlog(user_id, user_input, user_intent,request_id,json_response)
            return Response(json_response, content_type='application/json')
        else:
            text_response = f'{bot_response}'
            insert_to_botrequestlog(user_id, user_input, user_intent,request_id,text_response)
            return Response(text_response, content_type='text/plain')
    except Exception as e:
        return Response("Sorry, i am having trouble helping with that. I am taking a note of it to improve myself and help you better next time",content_type='text/plain')
# Run the Flask app if this script is the main module
    
@app.route('/activate_intent', methods=['POST'])
def activate_intent():
    try:
        data = load_data()
        request_data = request.json  # Assuming the request contains JSON data

        # Check if the request contains the 'intent_name'
        if 'intent_name' not in request_data:
            return jsonify({'error': 'Missing intent_name in request'}), 400

        intent_name = request_data['intent_name']
        if intent_name in data['intentList']:
            return jsonify({'message': f'Intent {intent_name} activated successfully'}), 200
        else:
            return jsonify({'error': f'Intent {intent_name} not found'}), 404

    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Function to load JSON data from file
def load_data():
    with open('intent_config.json', 'r') as file:
        data = json.load(file)
    return data

# Function to save JSON data to file
def save_data(data):
    with open('intent_config.json', 'w') as file:
        json.dump(data, file, indent=4)

def load_upsert_data():
    with open('intents.json', 'r') as file:
        data = json.load(file)
    return data

# Function to save JSON data to file
def upsert_data(data):
    with open('intents.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/insert_or_modify', methods=['POST'])
def insert_or_modify_record():
    try:
        data = load_upsert_data()
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
        upsert_data(data)

        return jsonify({'message': 'Record inserted/modified successfully'}), 200

    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_data', methods=['GET'])
def get_data():
    cwd = os.getcwd()
    print("Current working directory",cwd)
    try:
        with open('intents.json', 'r') as file:
            data = json.load(file)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/train_chatbot', methods=['GET'])
def trigger_training():
    train_chatbot_model()
    return "Chatbot training completed", 200
def train_chatbot_model():
    nltk.download('punkt')
    nltk.download('wordnet')
    from nltk.stem import WordNetLemmatizer

    lemmatizer = WordNetLemmatizer()
    intents = json.loads(open('intents.json').read())

    words = []
    classes = []
    documents = []
    ignoreLetters = ['?', '!', '.', ',']

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            wordList = nltk.word_tokenize(pattern)
            words.extend(wordList)
            documents.append((wordList, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    words = [lemmatizer.lemmatize(word) for word in words if word not in ignoreLetters]
    words = sorted(set(words))

    classes = sorted(set(classes))

    pickle.dump(words, open('words.pkl', 'wb'))
    pickle.dump(classes, open('classes.pkl', 'wb'))

    training = []
    outputEmpty = [0] * len(classes)

    for document in documents:
        bag = []
        wordPatterns = document[0]
        wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
        for word in words:
            bag.append(1) if word in wordPatterns else bag.append(0)

        outputRow = list(outputEmpty)
        outputRow[classes.index(document[1])] = 1
        training.append(bag + outputRow)

    random.shuffle(training)
    training = np.array(training)

    trainX = training[:, :len(words)]
    trainY = training[:, len(words):]

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(len(trainY[0]), activation='softmax'))

    sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    hist = model.fit(np.array(trainX), np.array(trainY), epochs=200, batch_size=5, verbose=1)
    model.save('chatbot_model.h5', hist)
    print('Training done')
    importlib.reload(chatbot)
    predict_class("test")

if __name__ == '__main__':
    app.run(debug=True)
