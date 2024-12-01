import os
import json
import subprocess
from flask import Flask, request, jsonify
import requests
import base64
import re
from leakcheck import LeakCheckAPI_v2
from flask import Flask, render_template,send_from_directory


app = Flask(__name__,static_folder='gui')


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
    
def query_leakcheck(email, type):
    
    api_key = os.getenv("API")
    if not api_key:
        raise ValueError("LEAKCHECK_API_KEY environment variable is not set!")
    api = LeakCheckAPI_v2(api_key)
    
    result = api.lookup(query=email, query_type=type, limit=10)
    print("Printing leakcheck results")
    print(result)
    
    print(email)
    #data = [{'source': {'name': 'lolzteam.net', 'breach_date': '2019-02', 'unverified': 0, 'passwordless': 1, 'compilation': 0}, 'username': 'retr0', 'email': 'rus.nevka@gmail.com', 'fields': ['username', 'email']}, {'password': 'A12345', 'source': {'name': 'DayZ.com', 'breach_date': '2016-03', 'unverified': 0, 'passwordless': 0, 'compilation': 0}, 'country': 'US', 'ip': '75.141.220.164', 'username': 'Retr0', 'email': 'dope_man_420@hotmail.com', 'fields': ['password', 'country', 'ip', 'username', 'email']}, {'password': '3177389', 'source': {'name': 'WiiHacks.com', 'breach_date': '2013-08', 'unverified': 0, 'passwordless': 0, 'compilation': 0}, 'ip': '81.103.114.35', 'username': 'retr0', 'email': 'dopey1467@gmail.com', 'fields': ['password', 'ip', 'username', 'email']}, {'password': 'vuth3', 'source': {'name': 'GamerzPlanet.net', 'breach_date': '2015-09', 'unverified': 0, 'passwordless': 0, 'compilation': 0}, 'ip': '76.23.79.233', 'username': 'retr0', 'email': 'prodigy.zach@gmail.com', 'fields': ['password', 'ip', 'username', 'email']}, {'password': 'Zelda99', 'source': {'name': 'Konduit', 'breach_date': '2020-04', 'unverified': 0, 'passwordless': 0, 'compilation': 0}, 'username': 'Retr0', 'email': 'jkimball1993@gmail.com', 'fields': ['password', 'username', 'email']}, {'password': 'howella6764', 'source': {'name': 'FFShrine.org', 'breach_date': '2015-09', 'unverified': 0, 'passwordless': 0, 'compilation': 0}, 'username': 'Retr0', 'email': 'oldzkoolz@yahoo.com', 'fields': ['password', 'username', 'email']}, {'password': 'Mamamia10', 'source': {'name': 'Mpgh.net', 'breach_date': '2015-10', 'unverified': 0, 'passwordless': 0, 'compilation': 0}, 'ip': '188.22.77.214', 'username': 'ReTr0', 'email': 'christoph.linzner@gmx.at', 'fields': ['password', 'ip', 'username', 'email']}, {'password': 'kentut', 'source': {'name': 'gPotato.com', 'breach_date': '2006-11', 'unverified': 0, 'passwordless': 0, 'compilation': 0}, 'username': 'retr0', 'email': 'dead_in_head@hotmail.com', 'fields': ['password', 'username', 'email']}, {'password': 'mtvqm7g9', 'source': {'name': 'PESGaming.com', 'breach_date': None, 'unverified': 0, 'passwordless': 0, 'compilation': 0}, 'ip': '62.254.64.14', 'username': 'retr0', 'email': 'jones_ufc@hotmail.com', 'fields': ['password', 'ip', 'username', 'email']}, {'password': 'kokelio', 'source': {'name': 'Exvagos.com', 'breach_date': '2022-07', 'unverified': 0, 'passwordless': 0, 'compilation': 0}, 'dob': '1000-01-01', 'username': 'retr0', 'email': 'kokelio@hotmail.com', 'fields': ['password', 'dob', 'username', 'email']}]
    #data = [{'source': {'name': 'Deezer.com', 'breach_date': '2019-09', 'unverified': 0, 'passwordless': 1, 'compilation': 0}, 'country': 'CA', 'dob': '1986-09-30', 'first_name': 'Mykhailo', 'last_name': 'Samoilenko', 'username': 'Mykhailo..Samoilenko', 'email': 'smykhailo@yahoo.com', 'fields': ['country', 'dob', 'first_name', 'last_name', 'username', 'email']}]
    return result


@app.route('/')
def serve_index():
    return app.send_static_file('index.html')




@app.route('/GetInformation', methods=['POST'])
def get_information():
    print(request.get_json())
    passwordList = []
    addressList = []
    usernameList = []
    emailList = []
    accountFoundList=[]

    data = {
    "passwords": passwordList,
    "addresses": addressList,
    "usernames": usernameList,
    "emails": emailList,
    "accounts_found": accountFoundList  
            }

    jsonInput = request.get_json()
    print("Checking usernames")

    print("Full JSON Input:", jsonInput)
    print("Type of 'usernames':", type(jsonInput['usernames']))
    print("Content of 'usernames':", jsonInput['usernames'])

    

    for username in jsonInput['usernames']:
        print(username)
        print(jsonInput)
        for entry in query_leakcheck(username, "username"):
            if 'email' in entry and entry['email'] != 'N/A' and entry['email'] not in emailList:
                emailList.append(entry['email'])
            if 'password' in entry and entry['password'] != 'N/A' and entry['password'] not in passwordList:
                passwordList.append(entry['password'])
            if 'address' in entry and entry['address'] != 'N/A' and entry['address'] not in addressList:
                addressList.append(entry['address'])
            if 'username' in entry and entry['username'] != 'N/A' and entry['username'] not in usernameList:
                usernameList.append(entry['username'])

    print("Checking emails")

    for email in jsonInput["emails"]:
        for entry in query_leakcheck(email, "email"):
            if 'email' in entry and entry['email'] != 'N/A' and entry['email'] not in emailList:
                emailList.append(entry['email'])
            if 'password' in entry and entry['password'] != 'N/A' and entry['password'] not in passwordList:
                passwordList.append(entry['password'])
            if 'address' in entry and entry['address'] != 'N/A' and entry['address'] not in addressList:
                addressList.append(entry['address'])
            if 'username' in entry and entry['username'] != 'N/A' and entry['username'] not in usernameList:
                usernameList.append(entry['username'])

    
    
    print("Checking Proxynova")    
    for SingleEmail in jsonInput["emails"]:
        proxynovaResponse = query_proxynova(SingleEmail)
        passwords = [line.split(":")[1] for line in proxynovaResponse["lines"]]
        for i in passwords:
            if i not in passwordList:
                passwordList.append(i)
    
    print("Runing sherlock ")
    print("skiping sherlock ")
    accountFoundList.append(run_sherlock(jsonInput["usernames"], "sherlockOutput"))
    print("Returning data")
    json_joint_data = json.dumps(data, indent=5)

    return json_joint_data

if __name__ == '__main__':
    app.run(debug=True)
