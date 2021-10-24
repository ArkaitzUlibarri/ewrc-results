import os
import sys
import requests
from pyquery import PyQuery as pq


def get_entry_info(base_url, event_id, entry_info_id):
    current_file = os.path.basename(__file__)
    current_file_name = os.path.splitext(current_file)[0]

    url = base_url + "/" + current_file_name + "/" + str(event_id) + "/" + entry_info_id

    try:
        print(url)
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    if response.status_code == 200:

        doc = pq(response.text)

        try:
            driver = doc("div.driver")
            driver_name = driver.find(".driver-info-driver-name")
            driver_id = driver_name.find('a').attr('href').split('/')[2].split('-')[0]

            codriver = doc("div.codriver")
            codriver_name = codriver.find(".driver-info-codriver-name")
            codriver_id = codriver_name.find('a').attr('href').split('/')[2].split('-')[0]

            return {'driver_id': driver_id, 'codriver_id': codriver_id}

        except Exception as e:
            raise e
