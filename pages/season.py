import os
import sys
import requests
import sqlite3
import datetime
from pyquery import PyQuery as pq
from models.event import Event


def insertEvents(base_url, dbPath, dbName, startSeason):
	currentFile = os.path.basename(__file__)
	currentFileName = os.path.splitext(currentFile)[0]

	for season in range(startSeason, datetime.datetime.now().year + 1):

		url = base_url + "/" + currentFileName + "/" + str(season) + "/" + dbName + "/"

		try:
			print(url)
			response = requests.get(url)
		except requests.exceptions.RequestException as e:
			print(e)
			sys.exit(1)

		if response.status_code == 200:

			doc = pq(response.text)

			try:
				db = sqlite3.connect(dbPath)
				cursor = db.cursor()
				
				#Events
				events = doc.items(".season-event")
				for index,event in enumerate(events,start=1):
					rally = Event(season,event,index)
					db.execute('''INSERT INTO events 
					(id,season,season_event_id,edition,name,asphalt,gravel,snow,ice,dates,entries,finish,created_at,updated_at,deleted_at) 
					VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', rally.getTuple());

				db.commit()

			except Exception as e:
				db.rollback()	
				raise e
			finally:
				db.close()
