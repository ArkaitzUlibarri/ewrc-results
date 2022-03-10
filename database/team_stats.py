import sqlite3
import definitions


def teams_stats(season, table):
    connection = sqlite3.connect(definitions.DB_PATH)

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


def teams_scratchs(season):
    return teams_stats(season, 'scratchs')


def teams_leaders(season):
    return teams_stats(season, 'leaders')


def teams_results(season, code):
    condition = ""
    if code == "winners":
        condition = "(e.result = '1')"
    elif code == "podiums":
        condition = "(e.result = '1' or e.result = '2' or e.result = '3')"

    connection = sqlite3.connect(definitions.DB_PATH)

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


def teams_podiums(season):
    return teams_results(season, 'podiums')


def teams_winners(season):
    return teams_results(season, 'winners')
