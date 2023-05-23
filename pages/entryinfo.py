import os

import page
from config import app


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def get_entry_info(event_id, entry_info_id):
    url = app.BASE_URL + "/" + get_current_filename() + "/" + str(event_id) + "/" + entry_info_id

    doc = page.do_request(url)

    if doc is not None:
        try:
            driver = doc("div.driver")
            driver_name = driver.find(".driver-info-driver-name")
            driver_id = driver_name.find('a').attr('href').split('/')[2].split('-')[0]

            codriver_id = None
            codriver = doc("div.codriver")
            if codriver.length:
                codriver_name = codriver.find(".driver-info-codriver-name")
                codriver_id = codriver_name.find('a').attr('href').split('/')[2].split('-')[0]

            return {'driver_id': driver_id, 'codriver_id': codriver_id}

        except Exception as e:
            raise e

