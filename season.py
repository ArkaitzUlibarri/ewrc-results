import os
import sys
import requests
import sqlite3
import datetime
import config
from pyquery import PyQuery as pq
from models.event import Event

currentfile = os.path.basename(__file__)
currentfilename = os.path.splitext(currentfile)[0]

os.system("cls")  # Clear console

for season in range(config.startSeason, datetime.datetime.now().year + 1):

	url = "https://www.ewrc-results.com/" + currentfilename + "/" + str(season) + "/" + config.database + "/"

	try:
		print(url)
		response = requests.get(url)
	except requests.exceptions.RequestException as e:
		print(e)
		sys.exit(1)

	if response.status_code == 200:

		doc = pq(response.text)

		try:
			db = sqlite3.connect(config.database + '.db')
			cursor = db.cursor()
			
			#Events
			events = doc.items(".season-event")
			for index,event in enumerate(events,start=1):
				rally = Event(season,event,index)
				db.execute('''INSERT INTO events 
				(id,season,season_event_id,edition,name,asphalt,gravel,snow,ice,dates,entries,finish) 
				VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', rally.getTuple());

			db.commit()

		except Exception as e:
			db.rollback()	
			raise e
		finally:
			db.close()
