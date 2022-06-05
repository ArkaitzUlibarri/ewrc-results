import sqlite3

import definitions


def up():

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS points(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            season INTEGER NOT NULL,
            overall_position_scoring JSON NOT NULL,
            group_position_scoring JSON NOT NULL,
            comments TEXT,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            CONSTRAINT points_unique UNIQUE (code,season))''')

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        print("Points table created")
        connection.close()
