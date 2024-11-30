# Read Input json File
import json
import glob

pattern = '*.json'
json_files = glob.glob(pattern)
fid_input = json_files[-1]
with open(fid_input, 'r') as file:
    data_gui = json.load(file)
emails_gui = data_gui['emails']
usernames_gui = data_gui['username']

emails = emails_gui.split(",")
usernames = usernames_gui.split(",")

data_in = {
    'usernames':usernames,
    'emails': emails,
    'first_name': data_gui['firstname'],
    'last_name': data_gui['lastname']}

with open('data_in.json', 'w') as json_file:
    json.dump(data_in, json_file, indent=4)
