from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route('/get_data', methods=['GET'])
def get_data():
    cwd = os.getcwd()
    print("Current working directory",cwd)
    try:
        with open('chatbot/intents.json', 'r') as file:
            data = json.load(file)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
