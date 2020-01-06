from PIL import Image
from PIL import ImageFile
import sys
import os
import sqlite3
from sqlite3 import Error

ImageFile.LOAD_TRUNCATED_IMAGES = True  

base_directory = os.getcwd()

CARD_ART_DIRECTORY = base_directory + "/MTG_card_art"

try:
    data_base_connection = sqlite3.connect(base_directory + "/card_image_data.db")
    data_base_cursor = data_base_connection.cursor()

    table = """ CREATE TABLE IF NOT EXISTS card_info (
                    card_name text,
                    card_set text, 
                    image_width integer,
                    image_height integer,
                    image_red integer,
                    image_green integer,
                    image_blue integer);"""

    data_base_cursor.execute(table)

    os.chdir(CARD_ART_DIRECTORY)

    card_set_list = os.listdir('.')

    for card_set in card_set_list:
        os.chdir(CARD_ART_DIRECTORY + "/" + card_set)
        for card_art in os.listdir('.'):
            print("Set: " + card_set + " -> Card Art: " + card_art)
            card_image = Image.open(card_art)
            width, height = card_image.size
            pixels = card_image.getcolors(width*height)
            most_frequent_pixel = pixels[0]

            for count, color in pixels:
                if count > most_frequent_pixel[0]:
                    most_frequent_pixel = (count, color)
			
            image_info = (card_art, card_set, width, height, most_frequent_pixel[1][0], most_frequent_pixel[1][1], most_frequent_pixel[1][2])
            print(image_info)
            print("\n")

            sql = ''' INSERT INTO card_info(card_name, card_set, image_width, image_height, image_red, image_green, image_blue)
                      VALUES(?,?,?,?,?,?,?);'''
            data_base_cursor = data_base_connection.cursor()
            data_base_cursor.execute(sql, image_info)
            data_base_connection.commit()


except Error as e:
    print(e)

finally:
    data_base_connection.close()
	

