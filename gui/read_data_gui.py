# Read Input GUI .json
import json
import glob

pattern = 'data_gui_raw*.json'
json_files = glob.glob(pattern)
fid_input = json_files[-1]
with open(fid_input, 'r') as file:
    data_gui = json.load(file)
emails_gui = data_gui['emails']
usernames_gui = data_gui['username']

emails = emails_gui.split(",")
usernames = usernames_gui.split(",")

data_gui_clean = {
    'usernames':usernames,
    'emails': emails,
    'first_name': data_gui['firstname'],
    'last_name': data_gui['lastname']}

# with open('data_gui_clean.json', 'w') as json_file:
#     json.dump(data_gui_clean, json_file, indent=4)
