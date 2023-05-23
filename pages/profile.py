import os

import page
from config import app
from models.driver import Driver
from services import driver_service


def get_current_filename():
	return os.path.splitext(os.path.basename(__file__))[0]


def insert_drivers(driver_list):
	for driver_id in driver_list:

		url = app.BASE_URL + "/" + get_current_filename() + "/" + str(driver_id)

		doc = page.do_request(url)

		if doc is not None and doc("main > div").eq(0).hasClass("profile"):

			# Header - Driver Info
			driver = Driver(doc, driver_id)
			driver_service.insert_drivers(driver.get_tuple())
