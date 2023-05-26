import sqlite3

import definitions


def get_season_stats(season, table):
    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""SELECT d.fullname,COUNT(stage_name) AS count
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


def get_season_scratchs(season):
    return get_season_stats(season, 'scratchs')


def get_season_leaders(season):
    return get_season_stats(season, 'leaders')


def get_season_results(season, code):
    condition = ""
    if code == "winners":
        condition = "(e.result = '1')"
    elif code == "podiums":
        condition = "(e.result = '1' or e.result = '2' or e.result = '3')"

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""SELECT d.fullname,COUNT(e.result) AS count
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


def get_season_podiums(season):
    return get_season_results(season, 'podiums')


def get_season_winners(season):
    return get_season_results(season, 'winners')


def get_drivers_in_points(season, points_position):
    connection = sqlite3.connect(definitions.DB_PATH)
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


def get_driver_season_results(season, driver_id):
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT 
                ev.id AS event_id,
                ev.season_order,
                ev.edition,
                ev.name,
                e.car_number,
                d.fullname AS driver,
                co.fullname AS codriver,
                e.plate,
                e.car,
                e.team,
                e.result
            FROM events AS ev
            LEFT JOIN entries AS e ON ev.id = e.event_id AND e.driver_id = :driver_id
            LEFT JOIN drivers AS d ON e.driver_id = d.id
            LEFT JOIN codrivers AS co ON e.codriver_id = co.id 
            WHERE ev.season = :season""", {"season": season, "driver_id": driver_id})

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

def get_driver_season_resume(season, driver_id):
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT 
            COUNT(ev.id) AS events, 
            COUNT(e.id) AS entries, 
            SUM(CASE WHEN e.result = '1' THEN 1 ELSE 0 END) AS wins,
            SUM(CASE WHEN e.result = '1' or e.result = '2' or e.result = '3' THEN 1 ELSE 0 END) AS podiums,
            SUM(CASE WHEN CAST(e.result AS INTEGER) <= 10 AND e.result GLOB '*[0-9]*' THEN 1 ELSE 0 END) AS point_position,
            SUM(CASE WHEN e.result GLOB '*[^0-9]*' THEN 1 ELSE 0 END) AS DNFs
            FROM events AS ev
            LEFT JOIN entries AS e ON ev.id = e.event_id AND e.driver_id = :driver_id
            LEFT JOIN drivers AS d ON e.driver_id = d.id
            LEFT JOIN codrivers AS co ON e.codriver_id = co.id 
            WHERE ev.season = :season""", {"season": season, "driver_id": driver_id})

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

def get_full_season_winners(season):
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        cursor = connection.cursor()

        cursor.execute("""SELECT 
            ev.season_order AS ID,
            ev.edition,
            ev.name,
            d.fullname,
            e.car,
            e.team
            FROM events AS ev
            LEFT JOIN entries AS e on ev.id = e.event_id 
            LEFT JOIN drivers AS d on e.driver_id = d.id 
            WHERE ev.season=? and e.result like '1' 
            ORDER BY ev.season_order""", (season,))

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
