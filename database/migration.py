import os
import sqlite3

def migrate(dbPath):

    try:

        db = sqlite3.connect(dbPath)

        cursor = db.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS events(
            id INTEGER NOT NULL PRIMARY KEY,
            season INTEGER NOT NULL,
            season_event_id INTEGER NOT NULL,
            edition INTEGER,
            name TEXT NOT NULL,
            asphalt BOOLEAN NOT NULL,
            gravel BOOLEAN NOT NULL,
            snow BOOLEAN NOT NULL,
            ice BOOLEAN NOT NULL,
            dates TEXT,
            entries TEXT,
            finish TEXT,
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

        cursor.execute('''CREATE TABLE IF NOT EXISTS results(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            driver_id INTEGER NOT NULL,
            codriver_id INTEGER,
            season INTEGER NOT NULL,
            dorsal TEXT,
            car TEXT NOT NULL,
            team TEXT,
            plate TEXT,
            chassis TEXT,
            category TEXT,
            result TEXT,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            FOREIGN KEY(driver_id) REFERENCES drivers(id),
            FOREIGN KEY(codriver_id) REFERENCES codrivers(id),
            FOREIGN KEY(event_id) REFERENCES events(id),
            CONSTRAINT results_unique UNIQUE (event_id,driver_id,codriver_id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS scratchs(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            stage_number TEXT NOT NULL,
            stage_name TEXT NOT NULL,
            driver_id INTEGER NOT NULL,
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
            driver_id INTEGER NOT NULL,
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
            car TEXT,
            team TEXT,
            plate TEXT,
            tyres TEXT,
            category TEXT,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            FOREIGN KEY(driver_id) REFERENCES drivers(id),
            FOREIGN KEY(codriver_id) REFERENCES codrivers(id),
            FOREIGN KEY(event_id) REFERENCES events(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS images(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp,
            FOREIGN KEY(event_id) REFERENCES events(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS driver_points(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            season INTEGER NOT NULL UNIQUE,
            overall_position_scoring json NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS powerstage_points(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            season INTEGER NOT NULL UNIQUE,
            overall_position_scoring json NOT NULL,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS manufacturer_points(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            season INTEGER NOT NULL UNIQUE,
            overall_position_scoring json NOT NULL,
            group_position_scoring json,
            comments TEXT,
            created_at timestamp,
            updated_at timestamp,
            deleted_at timestamp)''')

        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        print("Migration completed")
        db.close()
