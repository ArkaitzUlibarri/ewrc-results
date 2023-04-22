import sqlite3

import definitions


def select_nationality(nationality):
    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        cursor.execute("""SELECT id
        FROM nationalities 
        WHERE name = :nationality
        ORDER BY id DESC""", {"nationality": nationality})

        return cursor.fetchone()[0]

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def select_nationalities():
    connection = sqlite3.connect(definitions.DB_PATH)
    connection.row_factory = sqlite3.Row

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM nationalities ORDER BY id DESC")

        return cursor.fetchall()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

def replace_nationalities(nationality_tuple):

    connection = sqlite3.connect(definitions.DB_PATH)

    try:
        replace_statement = '''REPLACE INTO nationalities 
                (id,name,created_at,updated_at,deleted_at) 
                VALUES (?,?,?,?,?)'''

        connection.execute(replace_statement, nationality_tuple)

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()