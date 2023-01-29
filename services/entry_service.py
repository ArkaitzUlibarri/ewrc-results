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

def update_entries_with_result(result_tuple):

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        update_statement = '''UPDATE entries
                        SET result = :result,
                            entry_info_id = :entry_info_id,
                            updated_at = :updated_at
                        WHERE driver_id = :driver_id 
                        AND codriver_id = :codriver_id 
                        AND event_id = :event_id;'''

        cursor.execute(update_statement, result_tuple)

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

def insert_entries(entry_tuple):

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        insert = '''INSERT INTO entries 
                    (event_id,car_number,driver_id,codriver_id,car,team,plate,tyres,category,startlist_m,championship,created_at,updated_at,deleted_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        connection.execute(insert, entry_tuple)

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()