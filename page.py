import requests
import sys
from pyquery import PyQuery as pyQuery


def do_request(url):
    try:
        print("Page requested: " + url)
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    if response.status_code == 200:
        return pyQuery(response.text)
    else:
        print("Page not available: " + url)
        return None
