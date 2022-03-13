import sqlite3
import definitions


def select_nationalities():
    connection = sqlite3.connect(definitions.DB_PATH)
    connection.row_factory = sqlite3.Row

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM nationalities ORDER BY id DESC")

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

