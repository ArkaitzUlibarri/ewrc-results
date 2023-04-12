import sqlite3

import definitions


def get_season_stats(season, table):
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


def get_season_podiums(season):
    return get_season_results(season, 'podiums')


def get_season_winners(season):
    return get_season_results(season, 'winners')


def get_teams_in_points(season, points_position):
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""SELECT e.car,e.team
        FROM entries AS e
        INNER JOIN events AS ev ON e.event_id = ev.id AND ev.season is :season
        INNER JOIN drivers AS d ON e.driver_id = d.id
        WHERE CAST(e.result AS INTEGER) <= :points_position
        AND e.result  GLOB '*[0-9]*'
        AND e.startlist_m like 'M'
        GROUP BY e.team""", {"season": season, "points_position": points_position})

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

# FIXME
def get_team_season_results(season, team):
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT e.*
            FROM entries AS e
            INNER JOIN events AS ev ON e.event_id = ev.id AND ev.season is :season
            INNER JOIN drivers AS d ON e.driver_id = d.id
            WHERE e.startlist_m like 'M'
            AND e.team like :team
            ORDER BY event_id,result""", {"season": season, "team": team})

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
