import os
import sys
import requests
import sqlite3
import datetime
from pyquery import PyQuery as pq
from helpers.event import Event

def readStandings(doc):
	clasificaciones = doc("table.points.table_h")

def readStats(doc):
	tables = doc.items("div.points-stats > div.points-stats-table")
	for table in tables:
		title = table("h3").text()
		rows = table.items("tr")

		for row in rows:
			pos = row(".points-pos").text()
			#flag = row(".points-flag")
			driver = row('a').text()
			wins = row(".points-total-small").text()

currentfile = os.path.basename(__file__)
currentfilename = os.path.splitext(currentfile)[0]

os.system("cls")	# Clear console

for season in range(1973,datetime.datetime.now().year + 1):

	url = "https://www.ewrc-results.com/"+ currentfilename + "/"+ str(season) +"/1-wrc/"

	try:
		print(url)
		response = requests.get(url)
	except requests.exceptions.RequestException as e:
		print(e)
		sys.exit(1)

	if response.status_code == 200:

		doc = pq(response.text)

		try:
			db = sqlite3.connect('wrc.db')
			cursor = db.cursor()
			
			#Eventos
			events = doc.items(".season-event")
			for index,event in enumerate(events,start=1):
				rally = Event(season,event,index)
				rallytuple = (rally.event_id,rally.season,rally.season_event_id,rally.edition,rally.name,rally.asphalt,rally.gravel,rally.snow,rally.ice,rally.dates,rally.entries,rally.finish)
				db.execute("INSERT INTO events (id,season,season_event_id,edition,name,asphalt,gravel,snow,ice,dates,entries,finish) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",rallytuple);

			db.commit()

		except Exception as e:
			db.rollback()	
			raise e
		finally:
			db.close()