import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq
from models.scratch import Scratch
from models.leader import Leader

def insert_event_stats(base_url, db_path, event_ids_dict):
	currentfile = os.path.basename(__file__)
	currentfilename = os.path.splitext(currentfile)[0]

	for key in event_ids_dict:
		for event_id in event_ids_dict[key]:

			url = base_url + "/" + currentfilename + "/" + str(event_id) + "/"

			try:
				print(url)
				response = requests.get(url)
			except requests.exceptions.RequestException as e:
				print(e)
				sys.exit(1)

			if response.status_code == 200:

				doc = pq(response.text)

				try:
					db = sqlite3.connect(db_path)
					cursor = db.cursor()

					# Eventstats - Scratches
					scratches = doc("div.stats-wins").eq(0)

					for tr in scratches('tr').items():
						tr("td:last").remove()  # Empty
						drivers = set(tr("td:last > a").map(lambda i, e: pq(e).attr('href').split('/')[2].split('-')[0]))
						for driver_id in drivers:
							if driver_id:
								scratch = Scratch(tr,event_id, driver_id)
								db.execute('''INSERT INTO scratchs 
								(event_id,stage_number,stage_name,driver_id,created_at,updated_at,deleted_at) 
								VALUES (?,?,?,?,?,?,?)''', scratch.get_tuple());

					# Eventstats - Leaders
					leads = doc("div.stats-leads").eq(0)

					for tr in leads('tr').items():
						drivers = set(tr("td:last > a").map(lambda i, e: pq(e).attr('href').split('/')[2].split('-')[0]))
						for driver_id in drivers:
							if driver_id:
								leader = Leader(tr,event_id,driver_id)
								db.execute('''INSERT INTO leaders 
								(event_id,stage_number,stage_name,driver_id,created_at,updated_at,deleted_at) 
								VALUES (?,?,?,?,?,?,?)''', leader.get_tuple());

					db.commit()

				except Exception as e:
					db.rollback()	
					raise e
				finally:
					db.close()
