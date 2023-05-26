import sqlite3

import definitions


def get_all_time_winners():
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        cursor = connection.cursor()

        cursor.execute("""SELECT 
    ROW_NUMBER () OVER (ORDER BY ev.season ,ev.season_order) id,
    ev.season,
    ev.season_order,
    ev.edition,
    ev.name as rallye,
    d.fullname as driver,
    cd.fullname as codriver,
    e.car,
    e.team,
    e.tyres,
    e.car_number
    FROM events ev
    LEFT JOIN entries AS e on ev.id = e.event_id 
    LEFT JOIN drivers AS d on e.driver_id = d.id 
    LEFT JOIN codrivers AS cd on e.codriver_id = cd.id 
    WHERE e.result like '1'""")
        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def get_global_wins_by_driver():
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        cursor = connection.cursor()

        cursor.execute("""SELECT d.fullname,count() as wins
            FROM events ev
            LEFT JOIN entries AS e on ev.id = e.event_id 
            LEFT JOIN drivers AS d on e.driver_id = d.id 
            LEFT JOIN codrivers AS cd on e.codriver_id = cd.id 
            WHERE e.result like '1'
            GROUP BY d.fullname
            ORDER BY wins desc""")
        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def get_global_wins_by_tyres():
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        cursor = connection.cursor()

        cursor.execute("""SELECT e.tyres,count() as wins
            FROM events ev
            LEFT JOIN entries AS e on ev.id = e.event_id 
            LEFT JOIN drivers AS d on e.driver_id = d.id 
            LEFT JOIN codrivers AS cd on e.codriver_id = cd.id 
            WHERE e.result like '1'
            GROUP BY e.tyres
            ORDER BY wins desc""")
        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def global_results_by_driver(driver_id):
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT 
                ev.season,
                ev.season_order,
                ev.edition,
                ev.name,
                e.car_number,
                d.fullname AS driver,
                co.fullname AS codriver,
                e.plate,
                e.car,
                e.team,
                e.result,
				e.tyres
            FROM entries AS e
            LEFT JOIN events AS ev ON e.event_id = ev.id
            LEFT JOIN drivers AS d ON e.driver_id = d.id
            LEFT JOIN codrivers AS co ON e.codriver_id = co.id 
			WHERE e.driver_id = :driver_id
			ORDER BY ev.season,ev.season_order
			--scratchs&leaderships""", {"driver_id": driver_id})

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
