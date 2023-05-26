import datetime
import json
import logging
import sqlite3

import definitions


def select_event(event_id):
    event_ids_dict = {}

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT id,season FROM events WHERE id=?", (event_id,))

        row = cursor.fetchone()

        logging.debug(row)

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

            cursor.execute("SELECT id FROM events WHERE season=? ORDER BY season_order", (season,))

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


def get_season_events(season):
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT 
                ev.id,
                ev.season_order,
                ev.name
            FROM events AS ev
            WHERE ev.season=?
            ORDER BY ev.season_order""", (season,))

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def save_timetable(timetable_list, event_id):
    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        update = '''UPDATE events
        SET timetable = :timetable,
            updated_at = :updated_at
        WHERE
            id = :id'''

        cursor.execute(update, {
            "timetable": json.dumps({"itinerary": timetable_list}),
            "updated_at": datetime.datetime.now(),
            "id": event_id
        })
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
