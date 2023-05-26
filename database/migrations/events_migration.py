import logging
import sqlite3

import definitions


def up():

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS events(
            id INTEGER NOT NULL PRIMARY KEY,
            season INTEGER NOT NULL,
            season_order INTEGER NOT NULL,
            edition INTEGER,
            name TEXT NOT NULL,
            surface JSON NOT NULL,
            dates TEXT,
            timetable JSON NOT NULL,
            championship JSON NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp)''')

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        logging.info("Events table created")
        connection.close()
