import os
import sqlite3
import sys

import requests
from pyquery import PyQuery as pq

import definitions
from config import app
from models.driver import Driver


def get_current_filename():
	return os.path.splitext(os.path.basename(__file__))[0]


def insert_drivers(driver_list, category):
	for driver_id in driver_list:

		url = app.BASE_URL + "/" + get_current_filename() + "/" + str(driver_id) + "/" + category

		try:
			print(url)
			response = requests.get(url, verify=False)
		except requests.exceptions.RequestException as e:
			print(e)
			sys.exit(1)

		if response.status_code == 200:

			doc = pq(response.text)

			connection = sqlite3.connect(definitions.DB_PATH)

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
