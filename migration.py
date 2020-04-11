import os
import sqlite3
import config

os.system("cls")  # Clear console

try:

    db = sqlite3.connect(config.database + '.db')

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
        finish TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS drivers(
        id INTEGER NOT NULL PRIMARY KEY,
        fullname TEXT NOT NULL,
        name TEXT NOT NULL,
        lastname TEXT NOT NULL,
        birthdate TEXT NOT NULL,
        deathdate TEXT NOT NULL,
        nationality TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS results(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL,
        driver_id INTEGER NOT NULL,
        codriver TEXT NOT NULL,
        season INTEGER NOT NULL,
        dorsal TEXT,
        car TEXT NOT NULL,
        plate TEXT,
        team TEXT,
        category TEXT,
        result TEXT NOT NULL,
        FOREIGN KEY(driver_id) REFERENCES drivers(id),
        FOREIGN KEY(event_id) REFERENCES events(id),
        CONSTRAINT results_unique UNIQUE (event_id,driver_id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS scratchs(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL,
        stage_number TEXT NOT NULL,
        stage_name TEXT NOT NULL,
        driver_id INTEGER NOT NULL,
        FOREIGN KEY(driver_id) REFERENCES drivers(id),
        FOREIGN KEY(event_id) REFERENCES events(id),
        CONSTRAINT scratchs_unique UNIQUE (event_id,stage_number,driver_id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS leaders(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL,
        stage_number TEXT NOT NULL,
        stage_name TEXT NOT NULL,
        driver_id INTEGER NOT NULL,
        FOREIGN KEY(driver_id) REFERENCES drivers(id),
        FOREIGN KEY(event_id) REFERENCES events(id),
        CONSTRAINT leaders_unique UNIQUE (event_id,stage_number,driver_id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS entries(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL,
        car_number TEXT NOT NULL,
        driver_id INTEGER NOT NULL,
        codriver_id INTEGER,
        team TEXT,
        car TEXT,
        plate TEXT,
        category TEXT,
        FOREIGN KEY(driver_id) REFERENCES drivers(id),
        FOREIGN KEY(event_id) REFERENCES events(id))''')

    db.commit()

except Exception as e:
    db.rollback()
    raise e
finally:
    print("Migration completed")
    db.close()
