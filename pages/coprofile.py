import os
import sqlite3
import sys

import requests
from pyquery import PyQuery as pq

import definitions
from config import app
from models.driver import Driver


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def insert_codrivers(codriver_list, category):
    for codriver_id in codriver_list:

        url = app.BASE_URL + "/" + get_current_filename() + "/" + str(codriver_id) + "/" + category

        try:
            print(url)
            response = requests.get(url, verify=False)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        if response.status_code == 200:

            doc = pq(response.text)

            connection = sqlite3.connect(definitions.DB_PATH)

            try:

                if doc("main > div").eq(0).hasClass("profile"):
                    # Header - Codriver Info
                    codriver = Driver(doc, codriver_id)
                    connection.execute('''REPLACE INTO codrivers 
                        (id,fullname,name,lastname,birthdate,deathdate,nationality,created_at,updated_at,deleted_at) 
                        VALUES (?,?,?,?,?,?,?,?,?,?)''', codriver.get_tuple())

                connection.commit()

            except Exception as e:
                connection.rollback()
                raise e
            finally:
                connection.close()
