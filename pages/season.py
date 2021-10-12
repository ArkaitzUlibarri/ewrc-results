import os
import sys
import requests
import sqlite3
import datetime
from pyquery import PyQuery as pq
from models.event import Event


def get_seasons(base_url):
    current_file = os.path.basename(__file__)
    current_file_name = os.path.splitext(current_file)[0]

    url = base_url + "/" + current_file_name + "/"

    try:
        print(url)
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    if response.status_code == 200:

        doc = pq(response.text)

        output = list()

        try:
            header = doc('.justify-content-start').not_('.season-nat').not_('.season-sct').not_('.header-flags')
            badges = header.find('a.badge').items()

            for index, badge in enumerate(badges, start=1):
                season = int(badge.attr('href').split('/')[2])
                output.append(season)

            return output

        except Exception as e:
            print(str(e))
            return list()


def insert_nationalities(base_url, db_path, season):
    current_file = os.path.basename(__file__)
    current_file_name = os.path.splitext(current_file)[0]

    url = base_url + "/" + current_file_name + "/" + str(season) + "/"

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

                replace_statement = '''REPLACE INTO nationalities 
                (id,name,created_at,updated_at,deleted_at) 
                VALUES (?,?,?,?,?)'''

                connection.execute(replace_statement, tuple(nationality_dict.values()))

            connection.commit()

        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()


def insert_championships(base_url, db_path, season, nationality_code):
    current_file = os.path.basename(__file__)
    current_file_name = os.path.splitext(current_file)[0]

    url = base_url + "/" + current_file_name + "/" + str(season) + "/" + '?nat=' + str(nationality_code)

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
                replace_statement = '''REPLACE INTO championships 
                (id,code,name,created_at,updated_at,deleted_at) 
                VALUES (?,?,?,?,?,?)'''
                connection.execute(replace_statement, tuple(championship_dict.values()))

            connection.commit()

        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()


def insert_events(base_url, db_path, start_season, championship):
    current_file = os.path.basename(__file__)
    current_file_name = os.path.splitext(current_file)[0]

    for season in range(start_season, datetime.datetime.now().year + 1):

        url = base_url + "/" + current_file_name + "/" + str(season) + "/" + championship + "/"

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

                event_query = '''
                    REPLACE INTO events
                    (id,season,season_event_id,edition,name,asphalt,gravel,snow,ice,dates,entries,finish,timetable,created_at,updated_at,deleted_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

                event_championship_query = '''
                    INSERT INTO event_championship
                    (event_id,championship_id,championship_order,coefficient,created_at,updated_at,deleted_at)
                    VALUES (?,?,?,?,?,?,?)'''

                # Events
                events = doc.items(".season-event")
                for index, event in enumerate(events, start=1):
                    rally = Event(season, event, index)
                    connection.execute(event_query, rally.get_tuple())
                    for section in rally.sections:
                        connection.execute(event_championship_query, list(section.values()))

                connection.commit()

            except Exception as e:
                connection.rollback()
                raise e
            finally:
                connection.close()
