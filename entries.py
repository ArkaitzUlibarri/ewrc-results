import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq
from helpers.db_helpers import selectEvents

currentfile = os.path.basename(__file__)
currentfilename = os.path.splitext(currentfile)[0]

os.system("cls")	# Clear console

event_ids_dict = selectEvents('wrc.db')

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
				db = sqlite3.connect('wrc.db')
				cursor = db.cursor()
				
				#Entries
				startlist = doc("div.startlist")

				startlist('td.startlist-sections > span.r8_bold_red').parents('tr').remove()#Remove course cars
				first_category = startlist("tr:first > td.td_cent").text()#First car category

				for tr in startlist('tr').items():
					number = tr("td.r8").text()[1:]
					driver = tr('td:not([class]):first > a').text()
					driver_id = tr('td:not([class]):first > a').attr('href').split('/')[2].split('-')[0]
					codriver = tr('td:not([class]):last > a').text()

					codriver_id = None
					if(tr('td:not([class]):last > a').attr('href')):
						codriver_id = tr('td:not([class]):last > a').attr('href').split('/')[2].split('-')[0]
						
					team = tr("td.startlist-team").text()
					for item in team.split(" "):
						if(item in driver):
							team = None

					plate = None
					if(tr("td.bold > span").hasClass("startlist-chassis")):
						plate = tr("td.bold > span.startlist-chassis > a").text()
					car = tr("td.bold").remove("span.startlist-chassis").text()
					
					category = tr("td.td_cent").text()
					championship = tr("td.startlist-m").text()
					sections = tr("td.startlist-sections").text()

					entry_tuple = (event_id,number,driver_id,codriver_id,team,car,plate,category)
					if(driver_id):
						db.execute("INSERT INTO entries (event_id,car_number,driver_id,codriver_id,team,car,plate,category) VALUES (?,?,?,?,?,?,?,?)",entry_tuple);

				db.commit()

			except Exception as e:
				db.rollback()	
				raise e
			finally:
				db.close()
