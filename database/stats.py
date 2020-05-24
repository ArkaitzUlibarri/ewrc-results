import sqlite3
import datetime

def rallyWinners(database,season):

	try:
		db = sqlite3.connect(database)
		cursor = db.cursor()

		cursor.execute("""SELECT 
			events.season_event_id as ID,
			events.edition,
			events.name,
			drivers.fullname,
			results.car,
			results.team
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

def driversChampionshipPointsSystem(database,season):

	try:
		db = sqlite3.connect(database)
		db.row_factory = sqlite3.Row
		cursor = db.cursor()

		cursor.execute("""SELECT overall_position_scoring
			FROM driver_points
			WHERE season <= :season
			LIMIT 1""", {"season":season})

		return cursor.fetchone()[0]

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

def driversScratchs(database,season):
	return driversStats(database,season,'scratchs')

def driversLeaders(database,season):
	return driversStats(database,season,'leaders')

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

def driversPodiums(database,season):
	return driversResults(database,season,'podiums')

def driversWinners(database,season):
	return driversResults(database,season,'winners')

def fullResultsByDriver(database,season,driver_id):

	try:
		db = sqlite3.connect(database)
		db.row_factory = sqlite3.Row
		cursor = db.cursor()

		cursor.execute("""SELECT events.season_event_id as ID,events.edition,events.name,results.dorsal,drivers.fullname,codrivers.fullname,results.plate,results.car,results.team,results.result
			FROM events
			LEFT JOIN results on events.id = results.event_id
			LEFT JOIN drivers on results.driver_id = drivers.id
			LEFT JOIN codrivers on results.codriver_id = codrivers.id 
			WHERE  events.season = :season and drivers.id = :driver_id
			ORDER BY events.season,events.season_event_id""", {"season":season,"driver_id":driver_id})

		return cursor.fetchall()

	except Exception as e:
		db.rollback()	
		raise e
	finally:
		db.close()
