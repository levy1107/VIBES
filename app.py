
from functools import wraps
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import markdown
import hashlib # Import hashlib for secure hashing

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the raw API key from environment variables
RAW_API_KEY = os.getenv("API_KEY") # This API_KEY is for authenticating requests to this Flask application, not for authenticating with the Gemini model itself.

if RAW_API_KEY:
    # Hash the API key for secure comparison
    HASHED_API_KEY = hashlib.sha256(RAW_API_KEY.encode('utf-8')).hexdigest()
else:
    HASHED_API_KEY = None # Handle case where API_KEY is not set

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        incoming_api_key = request.headers.get('X-API-KEY')
        if incoming_api_key:
            hashed_incoming_api_key = hashlib.sha256(incoming_api_key.encode('utf-8')).hexdigest()
            if hashed_incoming_api_key == HASHED_API_KEY:
                return f(*args, **kwargs)
        return jsonify({"message": "API key is missing or invalid."}), 401
    return decorated_function

@app.route('/')
def index():
    # Read and parse the backlog.md file
    try:
        with open('backlog.md', 'r', encoding='utf-8') as f:
            backlog_content_md = f.read()
        backlog_content_html = markdown.markdown(backlog_content_md)
    except FileNotFoundError:
        backlog_content_html = "<p>No backlog items yet.</p>"
        
    return render_template('index.html', api_key=api_key, backlog_content=backlog_content_html)

@app.route('/submit', methods=['POST'])
@api_key_required
def submit():
    """
    Handles the submission of new instructions from the web form.
    """
    data = request.get_json()
    instruction = data.get('instruction')
    
    if instruction:
        # Append the new instruction to the backlog file
        with open('backlog.md', 'a', encoding='utf-8') as f:
            f.write(f"\n\n---\n\n- {instruction}")
        
        print(f"New instruction added to backlog.md")
        return jsonify({"message": "Instruction received successfully!"}), 200
    
    return jsonify({"message": "No instruction provided."}), 400

if __name__ == '__main__':
    # Before running for the first time, you should create a .env file
    # based on .env.example and set your own secret key.
    if not RAW_API_KEY:
        print("CRITICAL ERROR: API_KEY not found in .env file.")
        print("Please create a .env file and set the API_KEY variable.")
    else:
        app.run(debug=True, port=5001)

