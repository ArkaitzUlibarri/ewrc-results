import sqlite3
import definitions


def migrate():

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS entries(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            car_number TEXT,
            driver_id INTEGER NOT NULL,
            codriver_id INTEGER,
            entry_info_id INTEGER,
            car TEXT,
            team TEXT,
            plate TEXT,
            tyres TEXT,
            category TEXT,
            result TEXT,
            startlist_m TEXT,
            championship JSON NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            FOREIGN KEY(driver_id) REFERENCES drivers(id),
            FOREIGN KEY(codriver_id) REFERENCES codrivers(id),
            FOREIGN KEY(event_id) REFERENCES events(id))''')

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        print("Entries migration completed")
        connection.close()
