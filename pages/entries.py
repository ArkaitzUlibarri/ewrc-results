import os
import sys

import requests
from pyquery import PyQuery as pyQuery

from config import app
from models.entry import Entry
from services import entry_service


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def insert_entries(event_ids_dict, championship_list):
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

                doc = pyQuery(response.text)

                # Entries
                startlist = doc.find("table.results").eq(0)
                startlist('td.entry-sct > span.text-danger').parents('tr').remove()  # Remove course cars

                for tr in startlist('tr').items():
                    entry = Entry(event_id, tr, championship_list)
                    if entry.driver_id:
                        entry_service.insert_entries(entry.get_tuple())
            else:
                print("Page not available: " + url)
