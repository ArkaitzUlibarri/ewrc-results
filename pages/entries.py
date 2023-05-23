import os

import page
from config import app
from models.entry import Entry
from services import entry_service


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def insert_entries(event_ids_dict, championship_list):
    for key in event_ids_dict:
        for event_id in event_ids_dict[key]:

            url = app.BASE_URL + "/" + get_current_filename() + "/" + str(event_id) + "/"

            doc = page.do_request(url)

            if doc is not None:
                # Entries
                startlist = doc.find("table.results").eq(0)
                # Remove course cars
                startlist('td.entry-sct > span.text-danger').parents('tr').remove()

                for tr in startlist('tr').items():
                    entry = Entry(event_id, tr, championship_list)
                    if entry.driver_id:
                        entry_service.insert_entries(entry.get_tuple())
