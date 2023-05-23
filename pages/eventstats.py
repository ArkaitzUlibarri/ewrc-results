import os
import sqlite3

from pyquery import PyQuery as pyQuery

import definitions
import page
from config import app
from models.leader import Leader
from models.scratch import Scratch


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def insert_scratches(connection, event_id, items):
    for index, tr in enumerate(items, start=1):
        scratch = Scratch(tr, event_id, index, pyQuery)
        statement = '''INSERT INTO scratchs
				(event_id,stage_number,stage_name,driver_id,created_at,updated_at,deleted_at)
				VALUES (?,?,?,?,?,?,?)'''
        if scratch.drivers is not None:
            for driver_id in scratch.drivers:
                connection.execute(statement, scratch.get_tuple(driver_id))
        else:
            connection.execute(statement, scratch.get_tuple(None))


def insert_leaders(connection, event_id, items):
    for index, tr in enumerate(items, start=1):
        leader = Leader(tr, event_id, index, pyQuery)
        statement = '''INSERT INTO leaders
				(event_id,stage_number,stage_name,driver_id,created_at,updated_at,deleted_at)
				VALUES (?,?,?,?,?,?,?)'''
        if leader.drivers is not None:
            for driver_id in leader.drivers:
                connection.execute(statement, leader.get_tuple(driver_id))
        else:
            connection.execute(statement, leader.get_tuple(None))


def insert_event_stats(event_ids_dict):
    for key in event_ids_dict:
        for event_id in event_ids_dict[key]:

            url = app.BASE_URL + "/" + get_current_filename() + "/" + str(event_id) + "/"

            doc = page.do_request(url)

            if doc is not None:

                connection = sqlite3.connect(definitions.DB_PATH)

                try:

                    # EventStats - Scratches
                    scratches = doc("div.stats-wins").eq(0)
                    insert_scratches(connection, event_id, scratches('tr').items())

                    # Event stats - Leaders
                    leads = doc("div.stats-leads").eq(0)
                    insert_leaders(connection, event_id, leads('tr').items())

                    connection.commit()

                except Exception as e:
                    connection.rollback()
                    raise e
                finally:
                    connection.close()
