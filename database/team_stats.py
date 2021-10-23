import sqlite3


def teams_stats(database, season, table):
    connection = sqlite3.connect(database)

    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""SELECT ee.team,COUNT(s.driver_id) as count
            FROM """ + table + """ AS s
            LEFT JOIN events AS e on s.event_id = e.id
            LEFT JOIN entries AS ee on e.id = ee.event_id AND s.driver_id = ee.driver_id
            WHERE s.event_id in (select id from events where season = :season)
            GROUP BY ee.team
            ORDER BY count DESC""", {"season": season})

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def teams_scratchs(database, season):
    return teams_stats(database, season, 'scratchs')


def teams_leaders(database, season):
    return teams_stats(database, season, 'leaders')


def teams_results(database, season, code):
    condition = ""
    if code == "winners":
        condition = "(r.result = '1')"
    elif code == "podiums":
        condition = "(r.result = '1' or r.result = '2' or r.result = '3')"

    connection = sqlite3.connect(database)

    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""SELECT e.car,e.team,COUNT(e.team) as count
        FROM entries AS e
        INNER JOIN events AS ev ON e.event_id = ev.id AND ev.season is :season
        WHERE """ + condition + """
        GROUP BY e.team
        ORDER BY count DESC""", {"season": season})

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def teams_podiums(database, season):
    return teams_results(database, season, 'podiums')


def teams_winners(database, season):
    return teams_results(database, season, 'winners')
