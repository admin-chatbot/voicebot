# Import necessary modules
from flask import Flask, render_template, request
from chatbot import predict_class, get_response
from utilities import extract_entities, get_stock_data, generate_stock_response

# Initialize the Flask app
app = Flask(__name__)

# Function to make a curl request and parse the JSON response
# (No need to move this to utilities.py since it's specific to this script)

# Define the route for the home page
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

    # Check if the intent is related to "stocks"
    if processed_input[0]['intent'] == "stocks":
        # Extract named entities from user input
        entities = extract_entities(user_input)

        # Get the stock symbol (assuming it is part of the entities, modify as needed)
        #stock_symbol = entities[0] if entities else "AAPL"
        stock_symbol = "AAPL"

        # Make a curl request to fetch stock data using the specified symbol
        stock_data = get_stock_data(stock_symbol)

        # Generate a bot response with stock information
        bot_response = generate_stock_response(entities, stock_data)
    else:
        # If the intent is not related to stocks, get a general response from the chatbot
        bot_response = get_response(processed_input)

    # Render the template with user input and bot response
    return render_template('index.html', user_input=user_input, bot_response=bot_response)

# Run the Flask app if this script is the main module
if __name__ == '__main__':
    app.run(debug=True)
