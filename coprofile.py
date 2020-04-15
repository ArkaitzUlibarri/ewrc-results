import os
import sys
import requests
import sqlite3
import config
from pyquery import PyQuery as pq
from models.driver import Driver
from helpers.db_helpers import selectCodrivers		

currentfile = os.path.basename(__file__)
currentfilename = os.path.splitext(currentfile)[0]

os.system("cls")  # Clear console

codriverlist = selectCodrivers(config.database + '.db')

for codriver_id in codriverlist:

	url = "https://www.ewrc-results.com/" + currentfilename + "/" + str(codriver_id) + "/" + config.profile

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

				#Header - Codriver Info
				codriver = Driver(doc,codriver_id)
				db.execute("INSERT INTO codrivers (id,fullname,name,lastname,birthdate,deathdate,nationality) VALUES (?,?,?,?,?,?,?)", codriver.getTuple());

			db.commit()

		except Exception as e:
			db.rollback()	
			raise e
		finally:
			db.close()
