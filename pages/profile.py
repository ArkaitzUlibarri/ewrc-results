import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq
from models.driver import Driver
from models.result import Result


def insert_profiles(base_url, db_path, driverlist, category):
	currentfile = os.path.basename(__file__)
	currentfilename = os.path.splitext(currentfile)[0]

	for driver_id in driverlist:

		url = base_url + "/" + currentfilename + "/" + str(driver_id) + "/" + category

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

				if(doc("main > div").eq(0).hasClass("profile")):

					#Header - Driver Info
					driver = Driver(doc,driver_id)
					db.execute('''INSERT INTO drivers 
					(id,fullname,name,lastname,birthdate,deathdate,nationality,created_at,updated_at,deleted_at)
					VALUES (?,?,?,?,?,?,?,?,?,?)''', driver.get_tuple());

					#Salidas-WRC
					for season in doc.items("div.profile-season"):

						starts = season.nextAll('div.profile-starts').eq(0)

						for start in starts('div.profile-start-line').items():
							result = Result(driver.id, season, start)
							db.execute('''INSERT INTO results 
							(event_id,driver_id,codriver_id,season,dorsal,car,plate,team,chassis,category,result,created_at,updated_at,deleted_at)
							VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', result.get_tuple());

				db.commit()

			except Exception as e:
				db.rollback()
				raise e
			finally:
				db.close()
