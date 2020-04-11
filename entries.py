import os
import sys
import requests
import sqlite3
import config
from pyquery import PyQuery as pq
from models.entry import Entry
from helpers.db_helpers import selectEvents

currentfile = os.path.basename(__file__)
currentfilename = os.path.splitext(currentfile)[0]

os.system("cls")	# Clear console

event_ids_dict = selectEvents(config.database + '.db')

for key in event_ids_dict:
	for event_id in event_ids_dict[key]:

		url = "https://www.ewrc-results.com/"+ currentfilename + "/" + str(event_id) + "/"

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
				
				#Entries
				startlist = doc("div.startlist")
				startlist('td.startlist-sections > span.r8_bold_red').parents('tr').remove()#Remove course cars
				first_category = startlist("tr:first > td.td_cent").text()#First car category

				for tr in startlist('tr').items():
					entry = Entry(event_id,tr)
					entry_tuple = (entry.event_id,entry.car_number,entry.driver_id,entry.codriver_id,entry.team,entry.car,entry.plate,entry.category)
					if(entry.driver_id):
						db.execute("INSERT INTO entries (event_id,car_number,driver_id,codriver_id,team,car,plate,category) VALUES (?,?,?,?,?,?,?,?)",entry_tuple);

				db.commit()

			except Exception as e:
				db.rollback()	
				raise e
			finally:
				db.close()
