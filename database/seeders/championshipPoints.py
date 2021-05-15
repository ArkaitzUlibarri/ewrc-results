import datetime
import json
import os
import sqlite3


def seeder(db_path):
    package_dir = os.path.abspath(os.path.dirname(__file__))

    # Opening JSON file 
    f = open(os.path.join(package_dir, 'championshipPoints.json'), )

    # returns JSON object as a dictionary
    data = json.load(f)

    db = sqlite3.connect(db_path)

    try:

        cursor = db.cursor()

        for item in data['manufacturers']:
            cursor.execute('''REPLACE INTO manufacturer_points 
            (season,overall_position_scoring,group_position_scoring,comments,created_at,updated_at,deleted_at) 
            VALUES (?,?,?,?,?,?,?)''', [item['season'], json.dumps(item['overall_position_scoring']),
                                        json.dumps(item['group_position_scoring']), json.dumps(item['comments']),
                                        datetime.datetime.now(), datetime.datetime.now(), None])
            db.commit()

        for item in data['drivers']:
            cursor.execute('''REPLACE INTO driver_points 
            (season,overall_position_scoring,created_at,updated_at,deleted_at) 
            VALUES (?,?,?,?,?)''',
                           [item['season'], json.dumps(item['overall_position_scoring']), datetime.datetime.now(),
                            datetime.datetime.now(), None])
            db.commit()

        for item in data['powerstage']:
            cursor.execute('''REPLACE INTO powerstage_points 
            (season,overall_position_scoring,created_at,updated_at,deleted_at) 
            VALUES (?,?,?,?,?)''',
                           [item['season'], json.dumps(item['overall_position_scoring']), datetime.datetime.now(),
                            datetime.datetime.now(), None])
            db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    # Closing file 
    f.close()