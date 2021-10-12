import os
import json
import datetime
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq


def get_timetable(base_url, db_path, event_ids_dict):
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

                timetable = doc('.harm-main')

                day = ""
                event_legs = len(timetable('div.text-muted'))

                timetable_list = list()
                for div in timetable('div.harm.d-flex').items():
                    pending_legs = len(div.next_all('div.text-muted'))
                    leg = event_legs - pending_legs
                    date_first = div('div.harm-date:first')
                    hour = div('div.harm-date:last').text()
                    if date_first.text():
                        day = date_first.text()

                    if div('div.harm-ss').find('i'):
                        service_name = div('div.harm-stage').text()

                        timetable_item = {
                            "day": day,
                            "hour": hour,
                            "leg": leg,
                            "type": "Service",
                            "number": None,
                            "name": service_name,
                            "distance": None
                        }

                    else:
                        number = div('div.harm-ss').text()
                        stage_name = div('div.harm-stage').text()
                        distance = div('div.harm-km').text()

                        timetable_item = {
                            "day": day,
                            "hour": hour,
                            "leg": leg,
                            "type": "Stage",
                            "number": number,
                            "name": stage_name,
                            "distance": distance
                        }

                    timetable_list.append(timetable_item)

                save_timetable(db_path, timetable_list, event_id)


def save_timetable(db_path, timetable_item, event_id):
    connection = sqlite3.connect(db_path)

    try:

        cursor = connection.cursor()

        update = '''UPDATE events
        SET timetable = :timetable,
            updated_at = :updated_at
        WHERE
            id = :id'''

        cursor.execute(update, {
            "timetable": json.dumps(timetable_item),
            "updated_at": datetime.datetime.now(),
            "id": event_id
        })
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
