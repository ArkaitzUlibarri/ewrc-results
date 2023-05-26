import logging
import sqlite3

import definitions


def up():

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS scratchs(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            stage_number TEXT NOT NULL,
            stage_name TEXT NOT NULL,
            driver_id INTEGER,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            FOREIGN KEY(driver_id) REFERENCES drivers(id),
            FOREIGN KEY(event_id) REFERENCES events(id),
            CONSTRAINT scratchs_unique UNIQUE (event_id,stage_number,driver_id))''')

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        logging.info("Scratchs table created")
        connection.close()
