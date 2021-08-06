import sqlite3
import datetime


def select_event(database, event_id):
    event_ids_dict = {}

    connection = sqlite3.connect(database)

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


def select_events_info(database, event_id):
    connection = sqlite3.connect(database)
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


def select_events(database, start_season):
    event_ids_dict = {}

    connection = sqlite3.connect(database)

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


def select_drivers(database):
    connection = sqlite3.connect(database)

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT driver_id FROM scratchs")

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


def select_codrivers(database):
    connection = sqlite3.connect(database)

    try:

        cursor = connection.cursor()

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
        connection.rollback()
        raise e
    finally:
        connection.close()


def select_nationalities(database):

    connection = sqlite3.connect(database)

    try:

        cursor = connection.cursor()

        cursor.execute("""SELECT id
            FROM nationalities
            ORDER BY id DESC""")

        rows = cursor.fetchall()

        nationality_ids_list = []

        for row in rows:
            nationality_ids_list.append(row[0])

        return nationality_ids_list

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
