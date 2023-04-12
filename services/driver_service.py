import sqlite3

import definitions


def insert_drivers(driver_tuple):

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        statement = '''REPLACE INTO drivers 
					(id,fullname,name,lastname,birthdate,deathdate,nationality,created_at,updated_at,deleted_at)
					VALUES (?,?,?,?,?,?,?,?,?,?)'''

        connection.execute(statement, driver_tuple)

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

def insert_codrivers(codriver_tuple):

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        statement = '''REPLACE INTO codrivers 
                        (id,fullname,name,lastname,birthdate,deathdate,nationality,created_at,updated_at,deleted_at) 
                        VALUES (?,?,?,?,?,?,?,?,?,?)'''

        connection.execute(statement, codriver_tuple)

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()