import os
import sys

import requests
from pyquery import PyQuery as pq

from config import app
from services import event_service


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def insert_timetable(event_ids_dict):
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

                event_service.save_timetable(timetable_list, event_id)
            else:
                print("Page not available: " + url)
