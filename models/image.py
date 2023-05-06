import datetime
import os
import shutil
import sys

import requests
from pyquery import PyQuery as pyQuery

from config import app


def get_storage_path(event, file):
    season_folder = str(event['season'])
    event_folder = str(event['season_event_id']) + ' - ' + str(event['id']) + ' - ' + event['name']
    file_folder = os.path.join('storage', 'photos', season_folder, event_folder)
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    return os.path.join('storage', 'photos', season_folder, event_folder, file)


class Image:

    def __init__(self):
        self.id = None
        self.event_id = None
        self.driver_id = None
        self.codriver_id = None
        self.url = None
        self.content_url = None
        self.extension = None
        self.set_timestamps()

    def set_id(self, image_id):
        self.id = image_id
        self.url = app.BASE_URL + '/' + 'image' + '/' + self.id + '/'

    def set_event(self, event_id):
        self.event_id = event_id

    def get_driver_codriver(self):

        try:
            print(self.url)
            image_response = requests.get(self.url)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        if image_response.status_code == 200:
            image_doc = pyQuery(image_response.text)
            self.content_url = image_doc.find('#main-photo').find('img').attr('src')
            self.extension = self.content_url.rsplit('.')[-1]

            aside = image_doc.find('aside')
            for aside_link in aside.find('a').items():
                href = aside_link.attr('href')
                if app.BASE_URL in href:
                    href = href.split(app.BASE_URL)[1]
                if "coprofile" in href:
                    self.codriver_id = href.split('/')[2].split('-')[0]
                elif "profile" in href:
                    self.driver_id = href.split('/')[2].split('-')[0]

    def store_image(self, event_info):
        image_content = requests.get(self.content_url, stream=True)

        # Create target Directory if it doesn't exist
        file = self.id + '.' + self.extension
        storage_path = get_storage_path(event_info, file)

        with open(storage_path, 'wb+') as out_file:
            shutil.copyfileobj(image_content.raw, out_file)
        del image_content

    def set_timestamps(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.deleted_at = None

    def get_tuple(self):
        self.tuple = (
            self.id,
            self.event_id,
            self.driver_id,
            self.codriver_id,
            self.content_url,
            self.extension,
            self.created_at,
            self.updated_at,
            self.deleted_at
        )

        try:
            print(self.tuple)
        except Exception as e:
            print(e)

        return self.tuple
