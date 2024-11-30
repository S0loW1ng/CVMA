import os
import json
import subprocess
from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

# Replace these with your actual Dehashed API email and API key
DEHASHED_EMAIL = "your_email@example.com"
DEHASHED_API_KEY = "your_api_key"

DEHASHED_BASE_URL = "https://api.dehashed.com/search"

# Directory to store Sherlock results
SHERLOCK_RESULTS_DIR = "sherlock_results"
os.makedirs(SHERLOCK_RESULTS_DIR, exist_ok=True)

# Helper function to create the Basic Auth header
def create_auth_header(email, api_key):
    credentials = f"{email}:{api_key}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

# Helper function to run Sherlock
def run_sherlock(username_or_email, output_dir):
    try:
        # Run the Sherlock command
        subprocess.run(
            ["sherlock", username_or_email, "--output", os.path.join(output_dir, f"{username_or_email}.json")],
            check=True
        )
    except subprocess.CalledProcessError as e:
        return f"Error running Sherlock for {username_or_email}: {e}"
    return None

@app.route('/GetInformation', methods=['POST'])
def get_information():
    if not request.is_json:
        return jsonify({"error": "Invalid request. JSON payload required."}), 400
    
    data = request.get_json()
    query = data.get("query")
    
    if not query:
        return jsonify({"error": "Invalid JSON. 'query' field is required."}), 400
    
    # Construct the API URL with the query
    api_url = f"{DEHASHED_BASE_URL}?query={query}"
    
    try:
        # Make the GET request to the Dehashed API
        headers = create_auth_header(DEHASHED_EMAIL, DEHASHED_API_KEY)
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        dehashed_data = response.json()
        
        # Extract emails and usernames from Dehashed results
        emails = {entry.get("email") for entry in dehashed_data.get("entries", []) if entry.get("email")}
        usernames = {entry.get("username") for entry in dehashed_data.get("entries", []) if entry.get("username")}
        
        sherlock_errors = []
        
        # Run Sherlock for each username
        for username in usernames:
            error = run_sherlock(username, SHERLOCK_RESULTS_DIR)
            if error:
                sherlock_errors.append(error)
        
        # Return a summary of the results
        return jsonify({
            "emails": list(emails),
            "usernames": list(usernames),
            "sherlock_results_dir": SHERLOCK_RESULTS_DIR,
            "sherlock_errors": sherlock_errors,
        }), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error communicating with Dehashed API: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
