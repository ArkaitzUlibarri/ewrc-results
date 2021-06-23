import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq
from models.driver import Driver
from models.result import Result


def insert_profiles(base_url, db_path, driver_list, category):
	current_file = os.path.basename(__file__)
	current_file_name = os.path.splitext(current_file)[0]

	for driver_id in driver_list:

		url = base_url + "/" + current_file_name + "/" + str(driver_id) + "/" + category

		try:
			print(url)
			response = requests.get(url)
		except requests.exceptions.RequestException as e:
			print(e)
			sys.exit(1)

		if response.status_code == 200:

			doc = pq(response.text)

			try:
				connection = sqlite3.connect(db_path)
				cursor = connection.cursor()

				if doc("main > div").eq(0).hasClass("profile"):

					# Header - Driver Info
					driver = Driver(doc, driver_id)
					connection.execute('''INSERT INTO drivers 
					(id,fullname,name,lastname,birthdate,deathdate,nationality,created_at,updated_at,deleted_at)
					VALUES (?,?,?,?,?,?,?,?,?,?)''', driver.get_tuple())

					# Starts-WRC
					for season in doc.items("h5.profile-season"):

						starts = season.nextAll('div.profile-starts').eq(0)

						for start in starts('div.profile-start-line').items():
							result = Result(driver.id, season, start)
							connection.execute('''INSERT INTO results 
							(event_id,driver_id,codriver_id,season,car_number,car,plate,team,chassis,category,result,created_at,updated_at,deleted_at)
							VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', result.get_tuple())

				connection.commit()

			except Exception as e:
				connection.rollback()
				raise e
			finally:
				connection.close()
