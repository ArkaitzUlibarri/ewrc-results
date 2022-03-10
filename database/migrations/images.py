import sqlite3
import definitions


def migrate():

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS images(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            driver_id INTEGER,
            codriver_id INTEGER,
            content_url TEXT NOT NULL,
            extension TEXT NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            FOREIGN KEY(event_id) REFERENCES events(id))''')


        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        print("Images migration completed")
        connection.close()
