import sqlite3

import definitions


def select_drivers():
    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT driver_id FROM entries")

        rows = cursor.fetchall()

        driver_ids_list = []

        for row in rows:
            driver_ids_list.append(row[0])

        return driver_ids_list

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def select_codrivers():
    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT codriver_id FROM entries")

        rows = cursor.fetchall()

        driver_ids_list = []

        for row in rows:
            driver_ids_list.append(row[0])

        return driver_ids_list

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def select_events_without_results():

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT event_id FROM entries WHERE result IS NULL GROUP BY event_id ORDER BY event_id ASC")

        rows = cursor.fetchall()

        event_ids_list = []

        for row in rows:
            event_ids_list.append(row[0])

        return event_ids_list

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
