import json
import requests
from urllib import error
import os
import urllib.request
import time


base_directory = os.getcwd()

CARD_ART_DIRECTORY = base_directory + "/MTG_card_art"
CARD_SET_DIRECTORY = base_directory + "/card_set_info"

if os.path.isdir(CARD_ART_DIRECTORY) is False:
    os.mkdir("MTG_card_art")

os.chdir(CARD_SET_DIRECTORY)

card_set_list = os.listdir('.')

for card_set in card_set_list:
    os.chdir(CARD_SET_DIRECTORY)
    with open(card_set, 'r') as json_file:
        card_set_data = json.load(json_file)
    os.chdir(CARD_ART_DIRECTORY)
    if os.path.isdir(CARD_ART_DIRECTORY + "/" + card_set) is False:
        os.mkdir(card_set)
    os.chdir(card_set)
    for card in card_set_data:
        if "/" not in card["name"]:	
            try:
                if os.path.isfile(card["name"] + ".jpg") is False:
                    print("Downloading " + card["name"] + " from set " + card_set)
                    urllib.request.urlretrieve(card["image_uris"]["art_crop"], card["name"] + ".jpg")
            except (urllib.error.HTTPError, urllib.error.URLError) as error:
                print("Error occured. Retrying in 30 seconds.")
                print(error)
                time.sleep(30)
                urllib.request.urlretrieve(card["image_uris"]["art_crop"], card["name"] + ".jpg")
