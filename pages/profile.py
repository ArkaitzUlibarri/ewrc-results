import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq
from models.driver import Driver
from models.result import Result


def insert_drivers(base_url, db_path, driver_list, category):
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

			connection = sqlite3.connect(db_path)

			try:

				if doc("main > div").eq(0).hasClass("profile"):

					# Header - Driver Info
					driver = Driver(doc, driver_id)
					connection.execute('''REPLACE INTO drivers 
					(id,fullname,name,lastname,birthdate,deathdate,nationality,created_at,updated_at,deleted_at)
					VALUES (?,?,?,?,?,?,?,?,?,?)''', driver.get_tuple())

				connection.commit()

			except Exception as e:
				connection.rollback()
				raise e
			finally:
				connection.close()
