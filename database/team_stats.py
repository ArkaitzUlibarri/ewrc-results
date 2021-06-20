import sqlite3


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

        cursor.execute("""SELECT r.car,r.team,COUNT(r.team) as count
        FROM results r
        WHERE r.season is :season and """ + condition + """
        GROUP BY r.team
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
