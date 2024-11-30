# Read Input json File
import json
import glob

pattern = '*.json'
json_files = glob.glob(pattern)
fid_input = json_files[0]
with open(fid_input, 'r') as file:
    data = json.load(file)
emails_gui = data['emails']
usernames_gui = data['usernames']


print(data)

print('end')