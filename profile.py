import os
import sys
import requests
import sqlite3
import config
from pyquery import PyQuery as pq
from models.driver import Driver
from models.result import Result
from helpers.db_helpers import selectDrivers		

currentfile = os.path.basename(__file__)
currentfilename = os.path.splitext(currentfile)[0]

os.system("cls")  # Clear console

driverlist = selectDrivers(config.database + '.db')

for driver_id in driverlist:

	url = "https://www.ewrc-results.com/" + currentfilename + "/" + str(driver_id) + "/" + config.profile

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

			if(doc("main > div").eq(0).hasClass("profile")):

				#Header - Driver Info
				driver = Driver(doc,driver_id)
				db.execute("INSERT INTO drivers (id,fullname,name,lastname,birthdate,deathdate,nationality) VALUES (?,?,?,?,?,?,?)", driver.getTuple());

				#Salidas-WRC
				for season in doc.items("div.profile-season"):

					starts = season.nextAll('div.profile-starts').eq(0)

					for start in starts('div.profile-start-line').items():
						result = Result(driver.id, season, start)
						db.execute("INSERT INTO results (event_id,driver_id,codriver_id,season,dorsal,car,plate,team,chassis,category,result) VALUES (?,?,?,?,?,?,?,?,?,?,?)", result.getTuple());

			db.commit()

		except Exception as e:
			db.rollback()	
			raise e
		finally:
			db.close()
