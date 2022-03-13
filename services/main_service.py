import os
import sqlite3
import datetime
import definitions
from config import app


def select_event(event_id):
    event_ids_dict = {}

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT id,season FROM events WHERE id=?", (event_id,))

        row = cursor.fetchone()

        print(row)

        event_ids_dict[row[1]] = [row[0]]

        return event_ids_dict

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def select_events_info(event_id):
    connection = sqlite3.connect(definitions.DB_PATH)
    connection.row_factory = sqlite3.Row
    try:

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM events WHERE id=?", (event_id,))

        return cursor.fetchone()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def select_events(start_season):
    event_ids_dict = {}

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        for season in range(start_season, datetime.datetime.now().year + 1):

            cursor.execute("SELECT id FROM events WHERE season=? ORDER BY season_event_id", (season,))

            rows = cursor.fetchall()

            event_ids_list = []

            for row in rows:
                event_ids_list.append(row[0])

            event_ids_dict[season] = event_ids_list

        return event_ids_dict

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


def get_season_events(season):
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT 
                ev.id,
                ev.season_event_id,
                ev.name
            FROM events AS ev
            WHERE ev.season=?
            ORDER BY ev.season_event_id""", (season,))

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()