from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)       # Corrected Flask instantiation
CORS(app)                    # Enable CORS for all routes

@app.route('/hello')
def hello():
    return jsonify({"message": "Hello from Flask API!"})  # Fixed parentheses

if __name__ == "__main__":   # Corrected main check
    app.run(host='0.0.0.0', port=5000)  # Fixed quotes and comma
