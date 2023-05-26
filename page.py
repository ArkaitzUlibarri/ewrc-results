import requests
import sys
from pyquery import PyQuery as pyQuery
import logging


def do_request(url):
    try:
        logging.info("Page requested: " + url)
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.fatal(e)
        sys.exit(1)

    if response.status_code == 200:
        return pyQuery(response.text)
    else:
        logging.warning("Page not available: " + url)
        return None
