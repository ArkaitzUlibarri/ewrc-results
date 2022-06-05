import sqlite3

import definitions


def up():

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS nationalities(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp)''')

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        print("Nationalities table created")
        connection.close()
