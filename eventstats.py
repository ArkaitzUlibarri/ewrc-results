import os
import sys
import requests
import sqlite3
import datetime
import config
from pyquery import PyQuery as pq
from helpers.db_helpers import selectEvents

currentfile = os.path.basename(__file__)
currentfilename = os.path.splitext(currentfile)[0]

os.system("cls")	# Clear console

event_ids_dict = selectEvents(config.database + '.db')

for key in event_ids_dict:
	print(key)
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
				
				#Eventstats
				scratches = doc("div.stats-wins").eq(0)
				leads = doc("div.stats-leads").eq(0)
				
				for tr in scratches('tr').items():
					stage_number = tr("td:first > a").text()
					stage = tr("td.stats-stage1 > a").text()
					tr("td:last").remove()

					drivers = tr("td:last > a").items()
					driver_id = None
					for driver in drivers:
						if(driver_id != driver.attr('href').split('/')[2].split('-')[0]):
							driver_id = driver.attr('href').split('/')[2].split('-')[0]
							scratch_tuple = (event_id,stage_number,stage,driver_id)
							db.execute("INSERT INTO scratchs (event_id,stage_number,stage_name,driver_id) VALUES (?,?,?,?)",scratch_tuple);

				for tr in leads('tr').items():
					stage_number = tr("td:first > a").text()
					stage = tr("td.stats-stage2 > a").text()
					
					drivers = tr("td:last > a").items()
					driver_id = None
					for driver in drivers:
						if(driver_id != driver.attr('href').split('/')[2].split('-')[0]):
							driver_id = driver.attr('href').split('/')[2].split('-')[0]
							leader_tuple = (event_id,stage_number,stage,driver_id)
							db.execute("INSERT INTO leaders (event_id,stage_number,stage_name,driver_id) VALUES (?,?,?,?)",leader_tuple);

				db.commit()

			except Exception as e:
				db.rollback()	
				raise e
			finally:
				db.close()