# Import necessary modules
from flask import Flask, render_template, request, Response
from chatbot import predict_class, get_response
from utilities import  get_stock_data, generate_stock_response, generate_mongo_response, get_user_id_from_cookie
import spacy
from middleware.InitiateMiddleware import initiate_query_lookup,insert_to_botrequestlog
import json
from identity.decission import decision_module


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
        user_id = request.cookies.get('userId')
        print("request for user-", user_id)
        result = decision_module(request)
        if result=="clientID":
            return Response("requestClientID", content_type='text/plain')
        # Process user input using the chatbot's predict_class function
        client_id=result
        processed_input = predict_class(user_input)
        # Load intent list from intent_config.json
        intent_list=None
        user_intent=None
        with open("intent_config.json", "r") as intent_file:
            intent_config = json.load(intent_file)
            intent_list = intent_config.get("intentList", [])
        # Check if the intent is related to "stocks"
            user_intent=processed_input[0]['intent']
        if processed_input[0]['intent'] == "stocks":
            # Extract named entities from user input
            
            doc = nlp(user_input)
            entities = [ent.text for ent in doc.ents if ent.label_ == "ORG"]

            # Get the stock symbol (assuming it is part of the entities, modify as needed)
            #stock_symbol = entities[0] if entities else "AAPL"
            stock_symbol = "AAPL"

            # Make a curl request to fetch stock data using the specified symbol
            stock_data = get_stock_data(stock_symbol)

            # Generate a bot response with stock information
            bot_response = generate_stock_response(entities, stock_data)
        elif processed_input[0]['intent'] in intent_list:
            # Get the keyword field and value from your configuration
            keyword_field = "keyword"
            keyword_value = processed_input[0]['intent']

            # Call the initiatemiddleware function to retrieve data from MongoDB
            #results = initiate_query_lookup(keyword_field, keyword_value,client_id)
            results = initiate_query_lookup("keyword",  keyword_value,int(client_id))
            # Additional processing based on the MongoDB data can be added here if needed
            # For example, you can generate a response using the retrieved data

            # Example:
            bot_response = generate_mongo_response(results,keyword_value)

        else:
            # If the intent is not related to stocks, get a general response from the chatbot
            bot_response = get_response(processed_input)

        # Render the template with user input and bot response
        if isinstance(bot_response, dict):
            json_response = json.dumps(bot_response)
            insert_to_botrequestlog(user_id, user_input, user_intent)
            return Response(json_response, content_type='application/json')
        else:
            text_response = f'{bot_response}'
            insert_to_botrequestlog(user_id, user_input, user_intent)
            return Response(text_response, content_type='text/plain')
    except Exception as e:
        return Response("Sorry, i am having trouble helping with that. I am taking a note of it to improve myself and help you better next time",content_type='text/plain')
# Run the Flask app if this script is the main module
if __name__ == '__main__':
    app.run(debug=True)
