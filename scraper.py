import json
import requests
import os

if os.path.isfile('aether_revolt'):
	os.remove('aether_revolt')

response1 = requests.get("https://api.scryfall.com/sets/aer")
response1_data = response1.json()
response2 = requests.get(response1_data['search_uri'])

response2_data = response2.json()
response3 = requests.get(response2_data['next_page'])
response3_data = response3.json()

card_data = response2_data["data"] + response3_data["data"]

with open('aether_revolt', 'w') as outfile:
	json.dump(card_data, outfile, indent=4)

#import urllib.request
#urllib.request.urlretrieve(card_data[1]["image_uris"]["art_crop"], file_name)

