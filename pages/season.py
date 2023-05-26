import datetime
import logging
import os

import page
from config import app
from models.event import Event
from services import championship_service
from services import nationality_service


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def get_seasons():
    url = app.BASE_URL + "/" + get_current_filename() + "/"

    doc = page.do_request(url)

    if doc is not None:

        output = list()

        try:
            header = doc('.justify-content-start').not_('.season-nat').not_('.season-sct').not_('.header-flags')
            badges = header.find('a.badge').items()

            for index, badge in enumerate(badges, start=1):
                season = int(badge.attr('href').split('/')[2])
                output.append(season)

            return output

        except Exception as e:
            logging.info(str(e))
            return list()


def insert_nationalities(season):
    url = app.BASE_URL + "/" + get_current_filename() + "/" + str(season) + "/"

    doc = page.do_request(url)

    if doc is not None:

        header = doc('.justify-content-start.season-nat')
        badges = header.find('a.badge').items()

        for index, badge in enumerate(badges, start=1):
            code = badge.attr('href').split('/')[3].replace('?nat=', '')
            nationality = badge.text()
            nationality_dict = {
                'id': code,
                'name': nationality,
                'created_at': datetime.datetime.now(),
                'updated_at': datetime.datetime.now(),
                'deleted_at': None
            }

            nationality_service.replace_nationalities(tuple(nationality_dict.values()))


def insert_championships(season, nationality_code):
    url = app.BASE_URL + "/" + get_current_filename() + "/" + str(season) + "/" + '?nat=' + str(nationality_code)

    doc = page.do_request(url)

    if doc is not None:

        header = doc('.justify-content-start.season-sct')
        badges = header.find('.season-sct-item').find('a.badge').items()

        for index, badge in enumerate(badges, start=1):
            code = badge.attr('href').split('/')[3]
            championship_id = code.split('-')[0]
            championship = badge.text()
            championship_dict = {
                'id': championship_id,
                'code': code,
                'name': championship,
                'created_at': datetime.datetime.now(),
                'updated_at': datetime.datetime.now(),
                'deleted_at': None
            }

            championship_service.replace_championships(tuple(championship_dict.values()))


def insert_events(start_season, championship):
    for season in range(start_season, datetime.datetime.now().year + 1):

        url = app.BASE_URL + "/" + get_current_filename() + "/" + str(season) + "/" + championship + "/"

        doc = page.do_request(url)

        if doc is not None:

            # Events
            events = doc.items(".season-event")
            for index, event in enumerate(events, start=1):
                rally = Event()
                rally.save(season, event, index)
