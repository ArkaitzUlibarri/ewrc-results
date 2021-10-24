import json
import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq
from pages import entryinfo as entry_info_page
from models.entry import Entry


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

                    # Results
                    results = doc("div.final-results > table.results")
                    for tr in results('tr').items():
                        if tr('td:first').hasClass('body-background'):
                            continue
                        if tr('td:first').hasClass('final-results-stage'):
                            retirement_stage = tr('td.final-results-stage').text()
                            retirement_reason = tr("td.final-results-ret").text().replace('.', '')
                            result = retirement_stage + " - " + retirement_reason
                        else:
                            result = tr('td.font-weight-bold.text-left').text()

                        entry = tr('td.final-entry').text()
                        entry_info_id = tr('td.final-entry').find('a').attr('href').split('/')[3]
                        entry_info = entry_info_page.get_entry_info(base_url, event_id, entry_info_id)

                        update_statement = '''UPDATE entries
                                    SET result = :result
                                    WHERE driver_id = :driver_id 
                                    AND codriver_id = :codriver_id 
                                    AND event_id = :event_id;'''

                        cursor.execute(update_statement, {
                            "result": result,
                            "driver_id": entry_info["driver_id"],
                            "codriver_id": entry_info["codriver_id"],
                            "event_id": event_id,
                        })
                        connection.commit()
                except Exception as e:
                    connection.rollback()
                    raise e
                finally:
                    connection.close()
