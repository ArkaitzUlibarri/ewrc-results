import os
import sys
import requests
import sqlite3
import shutil
from pyquery import PyQuery as pq
from database.helper import select_events_info
from models.image import Image


def get_storage_path(event, file):
    season_folder = str(event['season'])
    event_folder = str(event['season_event_id']) + ' - ' + str(event['id']) + ' - ' + event['name']
    file_folder = os.path.join('storage', 'photos', season_folder, event_folder)
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    return os.path.join('storage', 'photos', season_folder, event_folder, file)


def insert_event_photos(base_url, db_path, event_ids_dict):
    current_file = os.path.basename(__file__)
    current_file_name = os.path.splitext(current_file)[0]

    for key in event_ids_dict:
        for event_id in event_ids_dict[key]:

            url = base_url + "/" + current_file_name + "/" + str(event_id) + "/"

            try:
                print(url)
                response = requests.get(url)
            except requests.exceptions.RequestException as e:
                print(e)
                sys.exit(1)

            if response.status_code == 200:

                doc = pq(response.text)

                connection = sqlite3.connect(db_path)

                try:

                    event_info = select_events_info(db_path, event_id)

                    # Event Photos
                    for photo in doc("div.photo-item").items():
                        image_id = photo.find('a').attr('href').split('/')[2]
                        image = Image(event_id, image_id, base_url)

                        insert_query = '''INSERT INTO images 
                        (id,event_id,driver_id,codriver_id,created_at,updated_at,deleted_at) 
                        VALUES (?,?,?,?,?,?,?)'''

                        connection.execute(insert_query, image.get_tuple())

                        # Image URL
                        # image_response = requests.get(image.url)
                        # if image_response.status_code == 200:
                        #     image_url = pq(image_response.text).find('#main-photo').find('img').attr('src')
                        #     extension = image_url.rsplit('.')[-1]
                        #
                        #     image_content = requests.get(image_url, stream=True)
                        #
                        #     # Create target Directory if don't exist
                        #     file = image_id + '.' + extension
                        #     storage_path = get_storage_path(event_info, file)
                        #
                        #     with open(storage_path, 'wb+') as out_file:
                        #         shutil.copyfileobj(image_content.raw, out_file)
                        #     del image_content

                    connection.commit()

                except Exception as e:
                    connection.rollback()
                    raise e
                finally:
                    connection.close()
