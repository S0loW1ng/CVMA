import os
import json
import subprocess
from flask import Flask, request, jsonify
import requests
import base64
import re

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
def run_sherlock(usernameList, output_dir):
    try:
        # Run the Sherlock command and capture output
        result = subprocess.run(
            ["sherlock", *usernameList],
            capture_output=True,
            text=True,  # Ensures output is a string instead of bytes
            check=True
        )

        # Save the terminal output to a file SO SLOW BUT THIS IS JUST TO TEST SHIT
        with open(output_dir, "w") as file:
            file.write(result.stdout)
        with open(output_dir, "r") as file:
            lines = file.readlines()
        filtered_lines = [line for line in lines if "[*]" not in line]


    except subprocess.CalledProcessError as e:
        # Save error message to the file if the command fails
        with open(output_dir, "w") as file:
            file.write(f"An error occurred:\n{e.stderr}")
        print(f"An error occurred. Check {output_dir} for details.")
    return  filtered_lines

def query_proxynova(email, start=0, limit=20):


    match = re.match(r"^([^@]+)@.+$", email)
    base_url = "https://api.proxynova.com/comb"
    params = {
        "query": match.group(1),
        "start": start,
        "limit": limit
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        reply = response.json()

        ##Debugung
        print("Proxynova request" + response.url)
        print(reply)

        return reply # Parse and return JSON response
    except requests.exceptions.RequestException as e:
        return {"error": f"Error communicating with ProxyNova API: {str(e)}"}
    
def query_leakcheck(email,limit,):
     # Replace these with your actual Dehashed API email and API key
    DEHASHED_EMAIL = "your_email@example.com"
    DEHASHED_API_KEY = os.getenv("DEHASHED_KEY")
    
    if not DEHASHED_API_KEY:
        raise ValueError("DEHASHED_KEY environment variable not set!")

    DEHASHED_BASE_URL = "https://api.dehashed.com/search"

    # Prepare the query parameters
    params = {
        "query": f"{field}:{query}",
        "limit": limit
    }

    # Create Basic Auth header
    auth_header = {
        "Authorization": "Basic " + base64.b64encode(f"{DEHASHED_EMAIL}:{DEHASHED_API_KEY}".encode()).decode()
    }

    try:
        # Make the GET request
        response = requests.get(DEHASHED_BASE_URL, headers=auth_header, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        reply = response.json()
    ##Debugung
        print("Dehashed request" + requests.Session().url)
        print(reply)
        # Return the JSON response
        return reply
    except requests.exceptions.RequestException as e:
        return {"error": f"Error communicating with Dehashed API: {str(e)}"}

''''
def query_dehashed(query, field="email", limit=20):

    # Replace these with your actual Dehashed API email and API key
    DEHASHED_EMAIL = "your_email@example.com"
    DEHASHED_API_KEY = os.getenv("DEHASHED_KEY")
    
    if not DEHASHED_API_KEY:
        raise ValueError("DEHASHED_KEY environment variable not set!")

    DEHASHED_BASE_URL = "https://api.dehashed.com/search"

    # Prepare the query parameters
    params = {
        "query": f"{field}:{query}",
        "limit": limit
    }

    # Create Basic Auth header
    auth_header = {
        "Authorization": "Basic " + base64.b64encode(f"{DEHASHED_EMAIL}:{DEHASHED_API_KEY}".encode()).decode()
    }

    try:
        # Make the GET request
        response = requests.get(DEHASHED_BASE_URL, headers=auth_header, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        reply = response.json()
    ##Debugung
        print("Dehashed request" + requests.Session().url)
        print(reply)
        # Return the JSON response
        return reply
    except requests.exceptions.RequestException as e:
        return {"error": f"Error communicating with Dehashed API: {str(e)}"}

        '''

@app.route('/GetInformation', methods=['POST'])
def get_information():
    passwordList = []
    hashesList = []
    usernameList = []
    emailList = []
    accountFoundList=[]

    data = {
    "passwords": passwordList,
    "hashes": hashesList,
    "usernames": usernameList,
    "emails": emailList,
    "accounts_found": accountFoundList  
            }

    jsonInput = request.get_json()
    print("Checking usernames")
    print("skip...")
    ''''
    for username in jsonInput["usernames"]:
        dehashedResponce = query_dehashed(username, field=username)
        for entry in dehashedResponce["entries"]:
                if entry.get("username"):  # Skip if username is empty or null
                    usernameList.append(entry["username"])
                if entry.get("password"):  # Skip if password is empty
                    passwordList.append(entry["password"])
                if entry.get("hashed_password"):  # Include hashes if present in data
                    hashesList.append(entry["hashed_password"])
                if entry.get("email"):
                    emailList.append(entry["hashed_password"])
                '''
    print("Checking Proxynova")    
    for SingleEmail in jsonInput["emails"]:
        proxynovaResponse = query_proxynova(SingleEmail)
        passwords = [line.split(":")[1] for line in proxynovaResponse["lines"]]
        for i in passwords:
            if i not in passwordList:
                passwordList.append(i)
    
    print("Runing sherlock ")
    accountFoundList.append(run_sherlock(jsonInput["usernames"], "sherlockOutput"))
    print("Returning data")
    json_joint_data = json.dumps(data, indent=5)

    return json_joint_data

if __name__ == '__main__':
    app.run(debug=True)
