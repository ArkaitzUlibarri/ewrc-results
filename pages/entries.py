import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq
from models.entry import Entry


def insert_entries(base_url, db_path, event_ids_dict):
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
				db = sqlite3.connect(db_path)

				try:

					cursor = db.cursor()

					# Entries
					startlist = doc("table.results")
					startlist('td.entry-sct > span.text-danger').parents('tr').remove()  # Remove course cars

					for tr in startlist('tr').items():
						entry = Entry(event_id, tr)
						if entry.driver_id:
							db.execute('''INSERT INTO entries 
							(event_id,car_number,driver_id,codriver_id,team,car,plate,tyres,category,created_at,updated_at,deleted_at)
							VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', entry.get_tuple());

					db.commit()

				except Exception as e:
					db.rollback()
					raise e
				finally:
					db.close()
