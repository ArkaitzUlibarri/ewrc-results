import sqlite3
import datetime

def selectEvents(database):

	event_ids_dict = {}

	try:
		db = sqlite3.connect(database)
		cursor = db.cursor()

		for season in range(1973,datetime.datetime.now().year + 1):

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

def rallyWinners(database,season):

	try:
		db = sqlite3.connect(database)
		cursor = db.cursor()

		cursor.execute("""SELECT events.season_event_id as ID,events.edition,events.name,drivers.fullname,results.car,results.team
			FROM events 
			LEFT JOIN results on events.id = results.event_id 
			LEFT JOIN drivers on results.driver_id = drivers.id 
			WHERE events.season=? and results.result like '1' 
			ORDER BY season_event_id""", (season,))
		 
		return cursor.fetchall()

	except Exception as e:
		db.rollback()	
		raise e
	finally:
		db.close()

def driversStats(database,season,table):

	try:
		db = sqlite3.connect(database)
		db.row_factory = sqlite3.Row
		cursor = db.cursor()

		cursor.execute("""SELECT drivers.fullname,COUNT(stage_name) as cuenta
			FROM """ + table + """ 
			INNER JOIN drivers on drivers.id = """ + table + """.driver_id
			WHERE event_id in (select id from events where season = :season)
			GROUP BY driver_id
			ORDER BY cuenta DESC""", {"season":season})
		 
		return cursor.fetchall()

	except Exception as e:
		db.rollback()	
		raise e
	finally:
		db.close()

def driversResults(database,season,result):

	if(result == "winners"):
		condition = "(result = '1')"
	elif(result == "podiums"):
		condition = "(result = '1' or result = '2' or result = '3')"

	try:
		db = sqlite3.connect(database)
		db.row_factory = sqlite3.Row
		cursor = db.cursor()

		cursor.execute("""SELECT drivers.fullname,COUNT(results.result) as cuenta
			FROM results
			INNER JOIN drivers on drivers.id = results.driver_id
			WHERE results.season is :season and """ + condition +"""
			GROUP BY drivers.fullname
			ORDER BY cuenta DESC""", {"season":season})
		 
		return cursor.fetchall()

	except Exception as e:
		db.rollback()	
		raise e
	finally:
		db.close()