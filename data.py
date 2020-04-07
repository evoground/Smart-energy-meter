import requests
import json

# def main():
# 	field = requests.get("https://api.thingspeak.com/channels/911165/feeds.json?api_key=YU00501VRICOT7DJ&results=2")
# 	field = field.json()
# 	return field['channel']

class Read_Data(object):
	"""docstring for Read_Data"""

	def read(self):
		field = requests.get("https://api.thingspeak.com/channels/911165/feeds.json?api_key=YU00501VRICOT7DJ&results=2")
		field = field.json()
		return field['feeds'][1]['field2']

		

