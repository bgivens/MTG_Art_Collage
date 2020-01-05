import json
import requests
import os

original_directory = os.getcwd()
#Need to make /card_set_info if it doesn't exist
os.chdir(original_directory+"/card_set_info")

mtg_set_list = requests.get("https://api.scryfall.com/sets").json()

for card_set in mtg_set_list["data"]:
    if "Tokens" not in card_set["name"]:
        print(card_set["name"])
        card_set_info = requests.get(card_set["search_uri"]).json()
	
        if "data" in card_set_info:
            set_card_list = card_set_info["data"]

            while "next_page" in card_set_info:
                card_set_info = requests.get(card_set_info["next_page"]).json()
                set_card_list = set_card_list + card_set_info["data"]
        if "/" not in card_set["name"]:
            with open(card_set["name"], 'w') as outfile:
                json.dump(set_card_list, outfile, indent=4)
    else:
        print("Skipping "+card_set["name"]+"...")

os.chdir(original_directory)
