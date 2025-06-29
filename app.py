
import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import markdown

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the secret key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route('/')
def index():
    """
    Reads the backlog.md file, converts it to HTML, and displays it.
    """
    try:
        with open('backlog.md', 'r', encoding='utf-8') as f:
            backlog_content = f.read()
        backlog_html = markdown.markdown(backlog_content)
    except FileNotFoundError:
        backlog_html = "<p>Error: backlog.md not found.</p>"
    
    return render_template('index.html', backlog_content=backlog_html)

@app.route('/submit', methods=['POST'])
def submit():
    """
    Handles the submission of new instructions from the web form.
    """
    instruction = request.form.get('instruction')
    submitted_password = request.form.get('password')

    # Security check
    if submitted_password != GEMINI_API_KEY:
        return "Unauthorized", 401

    if instruction:
        with open('new_instructions.md', 'w', encoding='utf-8') as f:
            f.write(instruction)
        
        # Here you would normally trigger the Gemini CLI to process the file.
        # For now, we'll just redirect back to the main page.
        print(f"New instruction received and saved to new_instructions.md")

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Before running for the first time, you should create a .env file
    # based on .env.example and set your own secret key.
    if not GEMINI_API_KEY:
        print("CRITICAL ERROR: GEMINI_API_KEY not found in .env file.")
        print("Please create a .env file and set the GEMINI_API_KEY variable.")
    else:
        app.run(debug=True, port=5001)
