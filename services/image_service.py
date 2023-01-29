import sqlite3

import definitions

def insert_images(image_tuple):
    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        insert_query = '''INSERT INTO images 
            (id,event_id,driver_id,codriver_id,content_url,extension,created_at,updated_at,deleted_at) 
            VALUES (?,?,?,?,?,?,?,?,?)'''

        connection.execute(insert_query, image_tuple)
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()