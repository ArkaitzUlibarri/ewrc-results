import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq
from models.driver import Driver	


def insert_codrivers(base_url, db_path, codriver_list, category):
	current_file = os.path.basename(__file__)
	current_file_name = os.path.splitext(current_file)[0]

	for codriver_id in codriver_list:

		url = base_url + "/" + current_file_name + "/" + str(codriver_id) + "/" + category

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

				if doc("main > div").eq(0).hasClass("profile"):
					# Header - Codriver Info
					codriver = Driver(doc, codriver_id)
					db.execute('''INSERT INTO codrivers 
					(id,fullname,name,lastname,birthdate,deathdate,nationality,created_at,updated_at,deleted_at) 
					VALUES (?,?,?,?,?,?,?,?,?,?)''', codriver.get_tuple());

				db.commit()

			except Exception as e:
				db.rollback()	
				raise e
			finally:
				db.close()
