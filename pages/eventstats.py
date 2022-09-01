import os
import sqlite3
import sys

import requests
from pyquery import PyQuery as pq

import definitions
from config import app
from models.leader import Leader
from models.scratch import Scratch


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def insert_scratches(connection, event_id, items):
    for index, tr in enumerate(items, start=1):
        scratch = Scratch(tr, event_id, index, pq)
        scratch_insert_query = '''INSERT INTO scratchs
				(event_id,stage_number,stage_name,driver_id,created_at,updated_at,deleted_at)
				VALUES (?,?,?,?,?,?,?)'''
        if scratch.drivers is not None:
            for driver_id in scratch.drivers:
                connection.execute(scratch_insert_query, scratch.get_tuple(driver_id))
        else:
            connection.execute(scratch_insert_query, scratch.get_tuple(None))


def insert_leaders(connection, event_id, items):
    for index, tr in enumerate(items, start=1):
        leader = Leader(tr, event_id, index, pq)
        leader_insert_query = '''INSERT INTO leaders
				(event_id,stage_number,stage_name,driver_id,created_at,updated_at,deleted_at)
				VALUES (?,?,?,?,?,?,?)'''
        if leader.drivers is not None:
            for driver_id in leader.drivers:
                connection.execute(leader_insert_query, leader.get_tuple(driver_id))
        else:
            connection.execute(leader_insert_query, leader.get_tuple(None))


def insert_event_stats(event_ids_dict):
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
