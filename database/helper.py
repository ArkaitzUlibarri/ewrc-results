import sqlite3
import datetime


def select_event(database, event_id):
    event_ids_dict = {}

    db = sqlite3.connect(database)

    try:

        cursor = db.cursor()

        cursor.execute("SELECT id,season FROM events WHERE id=?", (event_id,))

        row = cursor.fetchone()

        print(row)

        event_ids_dict[row[1]] = [row[0]]

        return event_ids_dict

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def select_events(database, start_season):
    event_ids_dict = {}

    db = sqlite3.connect(database)

    try:

        cursor = db.cursor()

        for season in range(start_season, datetime.datetime.now().year + 1):

            cursor.execute("SELECT id FROM events WHERE season=? ORDER BY season_event_id", (season,))

            rows = cursor.fetchall()

            event_ids_list = []

            for row in rows:
                event_ids_list.append(row[0])

            event_ids_dict[season] = event_ids_list

        return event_ids_dict

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def select_drivers(database):
    db = sqlite3.connect(database)

    try:

        cursor = db.cursor()

        cursor.execute("SELECT DISTINCT driver_id FROM scratchs")

        rows = cursor.fetchall()

        driver_ids_list = []

        for row in rows:
            driver_ids_list.append(row[0])

        return driver_ids_list

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def select_codrivers(database):
    db = sqlite3.connect(database)

    try:

        cursor = db.cursor()

        cursor.execute("""SELECT DISTINCT entries.codriver_id
			FROM entries
			INNER JOIN scratchs on entries.driver_id = scratchs.driver_id
			WHERE entries.codriver_id IS NOT NULL
			ORDER BY entries.codriver_id""")

        rows = cursor.fetchall()

        driver_ids_list = []

        for row in rows:
            driver_ids_list.append(row[0])

        return driver_ids_list

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
