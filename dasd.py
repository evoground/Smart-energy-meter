import json
import requests

with open('config.json','r+') as json_file:
	json_data = json.load(json_file)
	print(len(json_data))
	print(json_data['params']['admin_pass'])
	json_data['params']['admin_pass'] = "password"
	json_file.seek(0)
	# json.dump(json_data,json_file,indent = 2)
	json.dump(json_data,json_file)
	json_file.truncate()