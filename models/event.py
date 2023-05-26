import datetime
import json
import logging
import sqlite3
import definitions


class Event:

    def __init__(self):
        self.connection = sqlite3.connect(definitions.DB_PATH)
        self.event_id = None
        self.season = None
        self.season_order = None
        self.edition = None
        self.name = None
        self.dates = None
        self.surface = None
        self.asphalt = None
        self.gravel = None
        self.snow = None
        self.ice = None
        self.sections = {}
        self.timetable = {}
        self.created_at = None
        self.updated_at = None
        self.deleted_at = None
        self.tuple = ()

    def save(self, season, item, index):

        try:

            self.get_event_id(item)
            self.season = str(season)
            self.season_order = index
            self.get_event_name(item)
            self.get_event_surface(item)
            self.get_event_championships(item)
            self.set_timestamps()

            replace_statement = '''
                REPLACE INTO events
                (id,season,season_order,edition,name,surface,dates,timetable,championship,created_at,updated_at,deleted_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''

            self.connection.execute(replace_statement, self.get_tuple())
            self.connection.commit()

        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            self.connection.close()

    def get_event_id(self, item):
        self.event_id = item(".season-event-name a").attr('href').split('/')[2].split('-')[0]

    def get_event_name(self, item):
        event_name = item(".season-event-name").text().strip()

        self.name = event_name

        if "." in event_name:
            self.edition = event_name.split('.')[0]
            self.name = event_name.split('.')[1]

    def is_cancelled(self, item):
        for div in item.items("div"):
            if div.hasClass("widget-canceled"):
                return True
        return False

    def get_event_surface(self, item):
        info = item(".event-info").text()

        self.asphalt = "asphalt" in info or "tarmac" in info
        self.gravel = "gravel" in info
        self.snow = "snow" in info
        self.ice = "ice" in info

        self.surface = {
            "asphalt": self.asphalt,
            "gravel": self.gravel,
            "snow": self.snow,
            "ice": self.ice
        }

    def get_event_championships(self, item):
        self.sections = {}
        sections = list()
        event_championships = item(".event-sections a").items()
        for event_championship in event_championships:

            championship_id = int(event_championship.attr('href').split('/')[3].split('-')[0])

            championship = event_championship.text().strip()

            championship_order = None
            order_delimiter = "#"
            if order_delimiter in championship:
                start = championship.find(order_delimiter) + len(order_delimiter)
                end = championship.find(" ", start)
                if end == -1:
                    end = len(championship)
                championship_order = int(championship[start: end].strip())

            coefficient = None
            coefficient_delimiter = "coef"
            if coefficient_delimiter in championship:
                start = championship.find(coefficient_delimiter) + len(coefficient_delimiter)
                end = championship.find(")", start)
                coefficient = float(championship[start: end].strip().replace(',', '.'))

            sections.append({
                'id': championship_id,
                'order': championship_order,
                'coefficient': coefficient,
            })
        self.sections = {'championships': sections}

    def set_timestamps(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.deleted_at = None

    def get_tuple(self):
        self.tuple = (
            self.event_id,
            self.season,
            self.season_order,
            self.edition,
            self.name,
            json.dumps(self.surface),
            self.dates,
            json.dumps(self.timetable),
            json.dumps(self.sections),
            self.created_at,
            self.updated_at,
            self.deleted_at
        )

        try:
            logging.info(self.tuple)
        except Exception as e:
            logging.error(e)

        return self.tuple
