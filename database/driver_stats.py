import sqlite3


def season_winners(database, season):
    connection = sqlite3.connect(database)
    try:

        cursor = connection.cursor()

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
        connection.rollback()
        raise e
    finally:
        connection.close()


def championship_points_system(database, season, code):
    connection = sqlite3.connect(database)
    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""SELECT overall_position_scoring
            FROM points
            WHERE season <= :season AND code = :code
            ORDER BY season DESC
            LIMIT 1""", {"season": season, "code": code})

        return cursor.fetchone()[0]

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def drivers_stats(database, season, table):
    connection = sqlite3.connect(database)

    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""SELECT drivers.fullname,COUNT(stage_name) as count
            FROM """ + table + """ 
            INNER JOIN drivers on drivers.id = """ + table + """.driver_id
            WHERE event_id in (select id from events where season = :season)
            GROUP BY driver_id
            ORDER BY count DESC""", {"season": season})

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def drivers_scratchs(database, season):
    return drivers_stats(database, season, 'scratchs')


def drivers_leaders(database, season):
    return drivers_stats(database, season, 'leaders')


def drivers_results(database, season, code):
    condition = ""
    if code == "winners":
        condition = "(r.result = '1')"
    elif code == "podiums":
        condition = "(r.result = '1' or r.result = '2' or r.result = '3')"

    connection = sqlite3.connect(database)

    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""SELECT drivers.fullname,COUNT(r.result) as count
            FROM results r
            INNER JOIN drivers on drivers.id = r.driver_id
            WHERE r.season is :season and """ + condition + """
            GROUP BY drivers.fullname
            ORDER BY count DESC""", {"season": season})

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def drivers_podiums(database, season):
    return drivers_results(database, season, 'podiums')


def drivers_winners(database, season):
    return drivers_results(database, season, 'winners')


def full_results_by_driver(database, season, driver_id):
    connection = sqlite3.connect(database)
    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

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
        connection.rollback()
        raise e
    finally:
        connection.close()
