import sqlite3

import definitions


def championship_points_system(season, code):
    connection = sqlite3.connect(definitions.DB_PATH)
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
