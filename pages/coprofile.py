import os

import page
from config import app
from models.driver import Driver
from services import codriver_service


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def insert_codrivers(codriver_list):
    for codriver_id in codriver_list:

        url = app.BASE_URL + "/" + get_current_filename() + "/" + str(codriver_id) + "/"

        doc = page.do_request(url)

        if doc is not None and doc("main > div").eq(0).hasClass("profile"):
            # Header - Codriver Info
            codriver = Driver(doc, codriver_id)
            codriver_service.insert_codrivers(codriver.get_tuple())
