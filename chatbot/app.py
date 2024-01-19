# Import necessary modules
from flask import Flask, render_template, request, Response
from chatbot import predict_class, get_response
from utilities import  get_stock_data, generate_stock_response, generate_mongo_response
import spacy
from middleware.InitiateMiddleware import initiateQueryLookup
import json


# Initialize the Flask app
app = Flask(__name__)

# Function to make a curl request and parse the JSON response
# (No need to move this to utilities.py since it's specific to this script)

# Define the route for the home page
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
    return render_template('index.html')

# Define the route for handling user input and generating responses
@app.route('/chat', methods=['POST'])
def chat():
    # Get user input from the form
    user_input = request.form['user_input']

    # Process user input using the chatbot's predict_class function
    processed_input = predict_class(user_input)
    # Load intent list from intent_config.json
    intent_list=None
    with open("chatbot/intent_config.json", "r") as intent_file:
        intent_config = json.load(intent_file)
        intent_list = intent_config.get("intentList", [])
    # Check if the intent is related to "stocks"
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
        results = initiateQueryLookup(keyword_field, keyword_value)

        # Additional processing based on the MongoDB data can be added here if needed
        # For example, you can generate a response using the retrieved data

        # Example:
        bot_response = generate_mongo_response(results)

    else:
        # If the intent is not related to stocks, get a general response from the chatbot
        bot_response = get_response(processed_input)

    # Render the template with user input and bot response
    text_response = f'{bot_response}'

    return Response(text_response, content_type='text/plain')
# Run the Flask app if this script is the main module
if __name__ == '__main__':
    app.run(debug=True)
