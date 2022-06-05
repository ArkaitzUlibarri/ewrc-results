import sqlite3

import definitions


def drop_table(table):
    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute('DROP TABLE IF EXISTS ' + table)

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        print(table.capitalize() + " table dropped")
        connection.close()
