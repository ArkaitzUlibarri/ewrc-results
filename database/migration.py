import sqlite3


def migrate(db_path):

    connection = sqlite3.connect(db_path)

    try:

        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS events(
            id INTEGER NOT NULL PRIMARY KEY,
            season INTEGER NOT NULL,
            season_event_id INTEGER NOT NULL,
            edition INTEGER,
            name TEXT NOT NULL,
            surface JSON NOT NULL,
            dates TEXT,
            entries TEXT,
            finish TEXT,
            timetable JSON NOT NULL,
            championship JSON NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS drivers(
            id INTEGER NOT NULL PRIMARY KEY,
            fullname TEXT NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            birthdate TEXT,
            deathdate TEXT,
            nationality TEXT NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS codrivers(
            id INTEGER NOT NULL PRIMARY KEY,
            fullname TEXT NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            birthdate TEXT,
            deathdate TEXT,
            nationality TEXT NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS scratchs(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            stage_number TEXT NOT NULL,
            stage_name TEXT NOT NULL,
            driver_id INTEGER,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            FOREIGN KEY(driver_id) REFERENCES drivers(id),
            FOREIGN KEY(event_id) REFERENCES events(id),
            CONSTRAINT scratchs_unique UNIQUE (event_id,stage_number,driver_id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS leaders(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            stage_number TEXT NOT NULL,
            stage_name TEXT NOT NULL,
            driver_id INTEGER,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            FOREIGN KEY(driver_id) REFERENCES drivers(id),
            FOREIGN KEY(event_id) REFERENCES events(id),
            CONSTRAINT leaders_unique UNIQUE (event_id,stage_number,driver_id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS entries(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            car_number TEXT,
            driver_id INTEGER NOT NULL,
            codriver_id INTEGER,
            entry_info_id INTEGER,
            car TEXT,
            team TEXT,
            plate TEXT,
            tyres TEXT,
            category TEXT,
            result TEXT,
            startlist_m TEXT,
            championship JSON NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            FOREIGN KEY(driver_id) REFERENCES drivers(id),
            FOREIGN KEY(codriver_id) REFERENCES codrivers(id),
            FOREIGN KEY(event_id) REFERENCES events(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS images(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            driver_id INTEGER,
            codriver_id INTEGER,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            FOREIGN KEY(event_id) REFERENCES events(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS points(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            season INTEGER NOT NULL,
            overall_position_scoring JSON NOT NULL,
            group_position_scoring JSON NOT NULL,
            comments TEXT,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            CONSTRAINT points_unique UNIQUE (code,season))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS nationalities(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS championships(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp)''')

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        print("Migration completed")
        connection.close()
