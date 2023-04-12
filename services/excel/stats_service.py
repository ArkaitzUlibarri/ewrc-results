import sqlite3

import definitions


def get_all_time_winners():
    connection = sqlite3.connect(definitions.DB_PATH)
    try:

        cursor = connection.cursor()

        cursor.execute("""SELECT 
    ROW_NUMBER () OVER (ORDER BY ev.season ,ev.season_event_id) id,
    ev.season,
    ev.season_event_id,
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

