import os
import sys
import requests
import sqlite3
import shutil
from pyquery import PyQuery as pq
from database.helper import select_events_info
from models.image import Image


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

                    cursor = connection.cursor()

                    event_info = select_events_info(db_path, event_id)

                    # Event Photos
                    for photo in doc("div.photo-item").items():
                        image_id = photo.find('a').attr('href').split('/')[2]
                        image = Image(event_id, image_id, base_url)

                        # Image URL
                        image_response = requests.get(image.url)
                        if image_response.status_code == 200:
                            image_url = pq(image_response.text).find('#main-photo').find('img').attr('src')
                            extension = image_url.rsplit('.')[-1]

                            image_content = requests.get(image_url, stream=True)

                            # Create target Directory if don't exist
                            season_folder = str(event_info['season'])
                            event_folder = str(event_id) + ' - ' + event_info['name']
                            file = image_id + '.' + extension
                            if not os.path.exists(os.path.join('storage', 'photos', season_folder, event_folder)):
                                os.makedirs(os.path.join('storage', 'photos', season_folder, event_folder))

                            storage_path = os.path.join('storage', 'photos', season_folder, event_folder, file)

                            with open(storage_path, 'wb+') as out_file:
                                shutil.copyfileobj(image_content.raw, out_file)
                            del image_content

                        insert_query = '''INSERT INTO images (id,event_id,created_at,updated_at,deleted_at) VALUES (?,?,?,?,?)'''

                        connection.execute(insert_query, image.get_tuple())

                    connection.commit()

                except Exception as e:
                    connection.rollback()
                    raise e
                finally:
                    connection.close()
