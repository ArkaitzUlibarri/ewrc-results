import json
import os
import sys
import requests
import sqlite3
import datetime
from pyquery import PyQuery as pq
from pages import entryinfo as entry_info_page


def insert_results(base_url, db_path, event_ids_dict):
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

                    # Results table
                    results = doc("div.final-results > table.results")
                    for tr in results('tr').items():
                        # Entry info
                        entry = tr('td.final-entry')
                        if not entry.length:
                            continue
                        entry_info_id = entry.find('a').attr('href').split('/')[3]
                        entry_info = entry_info_page.get_entry_info(base_url, event_id, entry_info_id)

                        # Result info
                        if tr('td:first').hasClass('final-results-stage'):
                            retirement_stage = tr('td.final-results-stage').text()
                            retirement_reason = tr("td.final-results-ret").text().replace('.', '')
                            result = retirement_reason
                        else:
                            result = tr('td.font-weight-bold.text-left').not_(".final-results-number").text().replace('.', '')

                        update_statement = '''UPDATE entries
                                    SET result = :result,
                                        entry_info_id = :entry_info_id,
                                        updated_at = :updated_at
                                    WHERE driver_id = :driver_id 
                                    AND codriver_id = :codriver_id 
                                    AND event_id = :event_id;'''

                        cursor.execute(update_statement, {
                            "result": result,
                            "entry_info_id": int(entry_info_id),
                            "driver_id": entry_info["driver_id"],
                            "codriver_id": entry_info["codriver_id"],
                            "event_id": event_id,
                            "updated_at": datetime.datetime.now()
                        })

                        connection.commit()
                except Exception as e:
                    connection.rollback()
                    raise e
                finally:
                    connection.close()
