import sqlite3


def season_winners(database, season):
    connection = sqlite3.connect(database)
    try:

        cursor = connection.cursor()

        cursor.execute("""SELECT 
            ev.season_event_id as ID,
            ev.edition,
            ev.name,
            d.fullname,
            e.car,
            e.team
            FROM events AS ev
            LEFT JOIN entries AS e on ev.id = e.event_id 
            LEFT JOIN drivers AS d on e.driver_id = d.id 
            WHERE ev.season=? and e.result like '1' 
            ORDER BY ev.season_event_id""", (season,))

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

        cursor.execute("""SELECT d.fullname,COUNT(stage_name) as count
            FROM """ + table + """ 
            INNER JOIN drivers AS d on d.id = """ + table + """.driver_id
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

        cursor.execute("""SELECT d.fullname,COUNT(e.result) as count
            FROM entries AS e
            INNER JOIN drivers AS d on d.id = e.driver_id
            INNER JOIN events AS ev on e.event_id = ev.id AND ev.season is :season
            WHERE """ + condition + """
            GROUP BY d.fullname
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


def drivers_in_points(database, season, points_position):
    connection = sqlite3.connect(database)
    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""SELECT d.fullname,e.driver_id
        FROM entries AS e
        INNER JOIN events AS ev ON e.event_id = ev.id AND ev.season is :season
        INNER JOIN drivers AS d ON e.driver_id = d.id
        WHERE CAST(e.result AS INTEGER) <= :points_position 
        AND e.result  GLOB '*[0-9]*'
        GROUP BY e.driver_id""", {"season": season, "points_position": points_position})

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def full_results_by_driver(database, season, driver_id):
    connection = sqlite3.connect(database)
    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT ev.season_event_id as ID,ev.edition,ev.name,
            e.car_number,d.fullname,co.fullname,e.plate,e.car,e.team,e.result
            FROM events AS ev
            LEFT JOIN entries AS e on ev.id = e.event_id
            LEFT JOIN drivers AS d on e.driver_id = d.id
            LEFT JOIN codrivers AS co on e.codriver_id = co.id 
            WHERE ev.season = :season and d.id = :driver_id
            ORDER BY ev.season,ev.season_event_id""", {"season": season, "driver_id": driver_id})

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
