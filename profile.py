import os
import sys
import requests
import sqlite3
import config
from pyquery import PyQuery as pq
from models.driver import Driver
from models.result import Result
from helpers.db_helpers import selectDrivers		

def main(driverlist):
	currentfile = os.path.basename(__file__)
	currentfilename = os.path.splitext(currentfile)[0]

	#os.system("cls")	# Clear console

	for id in driverlist:

		url = "https://www.ewrc-results.com/"+ currentfilename + "/"+ str(id) +"/" + config.profile

		try:
			print(url)
			response = requests.get(url)
		except requests.exceptions.RequestException as e:
			print(e)
			sys.exit(1)

		if response.status_code == 200:

			doc = pq(response.text)

			if(doc("main > div").eq(0).hasClass("profile")):

				#Header
				driver = Driver(doc,id)

				#Titles
				titles = [t.text() for t in doc.items("div.profile-titles > div.profile-titles-overall > div.profile-titles-line > div.profile-titles-item")]

				#Estadisticas-WRC
				keys = [k.text().replace(":","") for k in doc.items("div.profile-stats > div.profile-stats-item > table> tr > td.td_right")]
				values = [v.text() for v in doc.items("div.profile-stats > div.profile-stats-item > table > tr > td.bold")]

				try:
					db = sqlite3.connect(config.database + '.db')
					cursor = db.cursor()	

					db.execute("INSERT INTO drivers (id,fullname,name,lastname,birthdate,deathdate,nationality) VALUES (?,?,?,?,?,?,?)", driver.getTuple());

					#Salidas-WRC
					for season in doc.items("div.profile-season"):

						starts = season.nextAll('div.profile-starts').eq(0)

						for start in starts('div.profile-start-line').items():
							result = Result(driver.id,season,start)
							db.execute("INSERT INTO results (event_id,driver_id,codriver,season,dorsal,car,plate,team,category,result) VALUES (?,?,?,?,?,?,?,?,?,?)", result.getTuple());

					db.commit()

				except Exception as e:
					db.rollback()	
					raise e
				finally:
					db.close()

driver_ids_list = selectDrivers(config.database + '.db')
main(driver_ids_list)