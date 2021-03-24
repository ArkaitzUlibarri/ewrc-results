import os
import sys
import requests
import sqlite3
import datetime
from pyquery import PyQuery as pq
from models.event import Event


def insert_events(base_url, db_path, db_name, start_season):
	current_file = os.path.basename(__file__)
	current_file_name = os.path.splitext(current_file)[0]

	for season in range(start_season, datetime.datetime.now().year + 1):

		url = base_url + "/" + current_file_name + "/" + str(season) + "/" + db_name + "/"

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
				
				#Events
				events = doc.items(".season-event")
				for index,event in enumerate(events,start=1):
					rally = Event(season,event,index)
					db.execute('''REPLACE INTO events 
					(id,season,season_event_id,edition,name,asphalt,gravel,snow,ice,dates,entries,finish,created_at,updated_at,deleted_at) 
					VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', rally.get_tuple());

				db.commit()

			except Exception as e:
				db.rollback()	
				raise e
			finally:
				db.close()
