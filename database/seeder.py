import datetime
import json
import os
import sqlite3


def championship_points(db_path):
    package_dir = os.path.abspath(os.path.dirname(__file__))

    # Opening JSON file 
    f = open(os.path.join(package_dir, 'seeders/championshipPoints.json'), )

    # returns JSON object as a dictionary
    data = json.load(f)

    connection = sqlite3.connect(db_path)

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

    print("Seeder Finished")
