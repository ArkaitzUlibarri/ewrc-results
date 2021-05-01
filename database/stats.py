import sqlite3
import datetime


def rally_winners(database, season):
    db = sqlite3.connect(database)
    try:

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


def drivers_championship_points_system(database, season):
    db = sqlite3.connect(database)
    try:

        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        cursor.execute("""SELECT overall_position_scoring
			FROM driver_points
			WHERE season <= :season
			LIMIT 1""", {"season": season})

        return cursor.fetchone()[0]

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def drivers_stats(database, season, table):
    db = sqlite3.connect(database)

    try:

        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        cursor.execute("""SELECT drivers.fullname,COUNT(stage_name) as count
			FROM """ + table + """ 
			INNER JOIN drivers on drivers.id = """ + table + """.driver_id
			WHERE event_id in (select id from events where season = :season)
			GROUP BY driver_id
			ORDER BY count DESC""", {"season": season})

        return cursor.fetchall()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def drivers_scratchs(database, season):
    return drivers_stats(database, season, 'scratchs')


def drivers_leaders(database, season):
    return drivers_stats(database, season, 'leaders')


def drivers_results(database, season, result):
    if result == "winners":
        condition = "(result = '1')"
    elif result == "podiums":
        condition = "(result = '1' or result = '2' or result = '3')"

    db = sqlite3.connect(database)

    try:

        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        cursor.execute("""SELECT drivers.fullname,COUNT(results.result) as count
			FROM results
			INNER JOIN drivers on drivers.id = results.driver_id
			WHERE results.season is :season and """ + condition + """
			GROUP BY drivers.fullname
			ORDER BY count DESC""", {"season": season})

        return cursor.fetchall()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def drivers_podiums(database, season):
    return drivers_results(database, season, 'podiums')


def drivers_winners(database, season):
    return drivers_results(database, season, 'winners')


def full_results_by_driver(database, season, driver_id):
    db = sqlite3.connect(database)
    try:

        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        cursor.execute("""
			SELECT events.season_event_id as ID,events.edition,events.name,
			results.dorsal,drivers.fullname,codrivers.fullname,results.plate,results.car,results.team,results.result
			FROM events
			LEFT JOIN results on events.id = results.event_id
			LEFT JOIN drivers on results.driver_id = drivers.id
			LEFT JOIN codrivers on results.codriver_id = codrivers.id 
			WHERE  events.season = :season and drivers.id = :driver_id
			ORDER BY events.season,events.season_event_id""", {"season": season, "driver_id": driver_id})

        return cursor.fetchall()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
