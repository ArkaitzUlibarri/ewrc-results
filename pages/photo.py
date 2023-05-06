import os
import sys

import requests
from pyquery import PyQuery as pq

from config import app
from models.image import Image
from services import event_service
from services import image_service


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def insert_event_photos(event_ids_dict):
    for key in event_ids_dict:
        for event_id in event_ids_dict[key]:

            url = app.BASE_URL + "/" + get_current_filename() + "/" + str(event_id) + "/"

            try:
                print(url)
                response = requests.get(url)
            except requests.exceptions.RequestException as e:
                print(e)
                sys.exit(1)

            if response.status_code == 200:

                doc = pq(response.text)

                event_info = event_service.select_events_info(event_id)

                # Event Photos
                for photo in doc("div.photo-item").items():
                    image = Image()
                    image_id = photo.find('a').attr('href').split('/')[2]
                    image.set_id(image_id)
                    image.set_event(event_id)
                    image.get_driver_codriver()

                    image_service.insert_images(image.get_tuple())

                    # image.store_image(event_info)

            else:
                print("Page not available: " + url)
