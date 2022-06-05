import datetime
import json
import os
import sqlite3

import definitions


def run():
    # Opening JSON file
    f = open(os.path.join(definitions.ROOT_DIR, 'database', 'seeds', 'championshipPoints.json'), )

    # returns JSON object as a dictionary
    data = json.load(f)

    connection = sqlite3.connect(definitions.DB_PATH)

    try:

        cursor = connection.cursor()

        insert = '''REPLACE INTO points 
           (code, season,overall_position_scoring,group_position_scoring,comments,created_at,updated_at,deleted_at) 
             VALUES (?,?,?,?,?,?,?,?)'''

        for code in data:
            for item in data[code]:
                parameters = [
                    code,
                    item['season'],
                    json.dumps(item['overall_position_scoring']),
                    json.dumps(item['group_position_scoring']),
                    json.dumps(item['comments']),
                    datetime.datetime.now(),
                    datetime.datetime.now(),
                    None
                ]
                cursor.execute(insert, parameters)
                connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

    # Closing file 
    f.close()

    print("Points seeder completed")
