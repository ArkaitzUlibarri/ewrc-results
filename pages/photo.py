import os
import sys
import requests
import sqlite3
import definitions
from pyquery import PyQuery as pq

from config import app
from database.helper import select_events_info
from models.image import Image


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def insert_event_photos(event_ids_dict):
    for key in event_ids_dict:
        for event_id in event_ids_dict[key]:

            url = app.base_url + "/" + get_current_filename() + "/" + str(event_id) + "/"

            try:
                print(url)
                response = requests.get(url)
            except requests.exceptions.RequestException as e:
                print(e)
                sys.exit(1)

            if response.status_code == 200:

                doc = pq(response.text)

                connection = sqlite3.connect(definitions.DB_PATH)

                try:

                    event_info = select_events_info(event_id)

                    # Event Photos
                    for photo in doc("div.photo-item").items():
                        image = Image()
                        image_id = photo.find('a').attr('href').split('/')[2]
                        image.set_id(image_id)
                        image.set_event(event_id)
                        image.get_driver_codriver()

                        insert_query = '''INSERT INTO images 
                            (id,event_id,driver_id,codriver_id,content_url,extension,created_at,updated_at,deleted_at) 
                            VALUES (?,?,?,?,?,?,?,?,?)'''

                        connection.execute(insert_query, image.get_tuple())
                        connection.commit()

                        image.store_image(event_info)

                except Exception as e:
                    connection.rollback()
                    raise e
                finally:
                    connection.close()
