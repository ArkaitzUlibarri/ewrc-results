import os
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

                for div in timetable('div.harm.d-flex').items():
                    pending_legs = len(div.next_all('div.text-muted'))
                    leg = event_legs - pending_legs
                    date_first = div('div.harm-date:first')
                    hour = div('div.harm-date:last').text()
                    if date_first.text():
                        day = date_first.text()

                    if div('div.harm-ss').find('i'):
                        service_name = div('div.harm-stage').text()

                        print(day + " " + hour + " Leg: " + str(leg) + " Service: " + service_name)
                    else:
                        number = div('div.harm-ss').text()
                        stage_name = div('div.harm-stage').text()
                        distance = div('div.harm-km').text()

                        print(day + " " + hour + " Leg: " + str(leg) + " Stage: " + number + " " + stage_name + " " + distance)
