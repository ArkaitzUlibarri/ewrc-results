import os
import sqlite3
import sys

import requests
from pyquery import PyQuery as pq

import definitions
from config import app
from models.entry import Entry


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def insert_entries(event_ids_dict, championship_list):
    for key in event_ids_dict:
        for event_id in event_ids_dict[key]:

            url = app.BASE_URL + "/" + get_current_filename() + "/" + str(event_id) + "/"

            try:
                print(url)
                response = requests.get(url, verify=False)
            except requests.exceptions.RequestException as e:
                print(e)
                sys.exit(1)

            if response.status_code == 200:

                doc = pq(response.text)
                connection = sqlite3.connect(definitions.DB_PATH)

                try:

                    # Entries
                    startlist = doc.find("table.results").eq(0)
                    startlist('td.entry-sct > span.text-danger').parents('tr').remove()  # Remove course cars

                    insert = '''INSERT INTO entries 
                                (event_id,car_number,driver_id,codriver_id,car,team,plate,tyres,category,startlist_m,championship,created_at,updated_at,deleted_at)
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

                    for tr in startlist('tr').items():
                        entry = Entry(event_id, tr, championship_list)
                        if entry.driver_id:
                            connection.execute(insert, entry.get_tuple())

                    connection.commit()

                except Exception as e:
                    connection.rollback()
                    raise e
                finally:
                    connection.close()
