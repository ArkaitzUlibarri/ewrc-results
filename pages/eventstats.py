import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq
from models.scratch import Scratch
from models.leader import Leader


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

				db = sqlite3.connect(db_path)

				try:

					cursor = db.cursor()

					# EventStats - Scratches
					scratches = doc("div.stats-wins").eq(0)

					for index, tr in enumerate(scratches('tr').items(), start=1):
						scratch = Scratch(tr, event_id, index, pq)
						scratch_insert_query = '''INSERT INTO scratchs
								(event_id,stage_number,stage_name,driver_id,created_at,updated_at,deleted_at)
								VALUES (?,?,?,?,?,?,?)'''
						if scratch.drivers is not None:
							for driver_id in scratch.drivers:
								scratch.get_tuple(driver_id)
								# db.execute(scratch_insert_query, scratch.get_tuple(driver_id))
						else:
							scratch.get_tuple(None)
							# db.execute(scratch_insert_query, scratch.get_tuple(None))

					# Eventstats - Leaders
					leads = doc("div.stats-leads").eq(0)

					for index, tr in enumerate(leads('tr').items(), start=1):
						leader = Leader(tr, event_id, index, pq)
						leader_insert_query = '''INSERT INTO leaders
								(event_id,stage_number,stage_name,driver_id,created_at,updated_at,deleted_at)
								VALUES (?,?,?,?,?,?,?)'''
						if leader.drivers is not None:
							for driver_id in leader.drivers:
								leader.get_tuple(driver_id)
								# db.execute(leader_insert_query, leader.get_tuple(driver_id))
						else:
							leader.get_tuple(None)
							# db.execute(leader_insert_query, leader.get_tuple(None))

					db.commit()

				except Exception as e:
					db.rollback()	
					raise e
				finally:
					db.close()
