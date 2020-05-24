import sqlite3
import datetime

def selectEvents(database, startSeason):

	event_ids_dict = {}

	try:
		db = sqlite3.connect(database)
		cursor = db.cursor()

		for season in range(startSeason, datetime.datetime.now().year + 1):

			cursor.execute("SELECT id FROM events WHERE season=? ORDER BY season_event_id", (season,))

			rows = cursor.fetchall()

			event_ids_list = []

			for row in rows:
				event_ids_list.append(row[0])

			event_ids_dict[season] = event_ids_list

		return event_ids_dict

	except Exception as e:
		db.rollback()	
		raise e
	finally:
		db.close()

def selectDrivers(database):

	try:
		db = sqlite3.connect(database)
		cursor = db.cursor()

		cursor.execute("SELECT DISTINCT driver_id FROM scratchs")

		rows = cursor.fetchall()

		driver_ids_list = []

		for row in rows:
			driver_ids_list.append(row[0])

		return driver_ids_list

	except Exception as e:
		db.rollback()	
		raise e
	finally:
		db.close()

def selectCodrivers(database):

	try:
		db = sqlite3.connect(database)
		cursor = db.cursor()

		cursor.execute("""SELECT DISTINCT entries.codriver_id
			FROM entries
			INNER JOIN scratchs on entries.driver_id = scratchs.driver_id
			WHERE entries.codriver_id IS NOT NULL
			ORDER BY entries.codriver_id""")

		rows = cursor.fetchall()

		driver_ids_list = []

		for row in rows:
			driver_ids_list.append(row[0])

		return driver_ids_list

	except Exception as e:
		db.rollback()	
		raise e
	finally:
		db.close()
