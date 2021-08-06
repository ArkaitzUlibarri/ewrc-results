import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq
from models.scratch import Scratch
from models.leader import Leader


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


def insert_event_stats(base_url, db_path, event_ids_dict):
	current_file = os.path.basename(__file__)
	current_filename = os.path.splitext(current_file)[0]

	for key in event_ids_dict:
		for event_id in event_ids_dict[key]:

			url = base_url + "/" + current_filename + "/" + str(event_id) + "/"

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

					# EventStats - Scratches
					scratches = doc("div.stats-wins").eq(0)
					insert_scratches(connection, event_id, scratches('tr').items())

					# Eventstats - Leaders
					leads = doc("div.stats-leads").eq(0)
					insert_leaders(connection, event_id, leads('tr').items())

					connection.commit()

				except Exception as e:
					connection.rollback()
					raise e
				finally:
					connection.close()
