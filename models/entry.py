import datetime
import json
import logging


def get_href_id(a_tag):
    return a_tag.attr('href').split('/')[2].split('-')[0]


def get_tyres(img_tag):
    return img_tag.attr('src').split('/')[5].split('.')[0].split('_')[0].upper()


def search_by_key(list_haystack, needle, search_key, return_key):
    for index, row in enumerate(list_haystack, start=1):
        if row[search_key] == needle:
            return row[return_key]
    return False


class Entry:

    def __init__(self, event_id, row, championship_list):

        car_number = row('td:first')
        entry = row('td.startlist-entry')
        driver = entry.find('div.startlist-driver').eq(0)
        codriver = entry.find('div.startlist-driver').eq(1)
        car_image = row('td.startlist-icon').find('img').attr('src')
        car = row("td.font-weight-bold.lh-130")
        team = car.find('span')
        plate = row("td.startlist-team").find('a')
        tyres = row("td.startlist-team").find('img')
        category = row("td.fs-091:first")
        startlist_m = row("td.startlist-m")
        championship = row("td.entry-sct")

        self.event_id = event_id
        self.car_number = None
        if car_number.text()[1:]:
            self.car_number = car_number.text()[1:]

        self.driver_id = None
        if row('div.startlist-driver:first > a').attr('href'):
            self.driver_id = get_href_id(driver.find('a'))

        self.codriver_id = None
        if row('div.startlist-driver:last > a').attr('href'):
            self.codriver_id = get_href_id(codriver.find('a'))

        self.car_image = car_image
        self.car = car.clone().find('span').remove().end().text()

        self.team = None
        self.plate = None
        self.tyres = None
        self.category = None
        self.startlist_m = None
        self.championship = {}

        if team:
            self.team = team.text()
        if plate:
            self.plate = plate.text()
        if tyres:
            self.tyre_image = tyres.attr('src')
            self.tyres = get_tyres(tyres)
        if category.text():
            self.category = category.text()
        if startlist_m.text():
            self.startlist_m = startlist_m.text()
        if championship.html():
            entry_championship_list = list()
            for championship_name in championship.text().splitlines():
                championship_id = search_by_key(championship_list, championship_name, 'name', 'id')
                entry_championship_list.append(championship_id)
            self.championship = {'championship': entry_championship_list}

        self.set_timestamps()

    def set_timestamps(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.deleted_at = None

    def get_tuple(self):
        self.tuple = (
            self.event_id,
            self.car_number,
            self.driver_id,
            self.codriver_id,
            self.car,
            self.team,
            self.plate,
            self.tyres,
            self.category,
            self.startlist_m,
            json.dumps(self.championship),
            self.created_at,
            self.updated_at,
            self.deleted_at
        )

        try:
            logging.info(self.tuple)
        except Exception as e:
            logging.error(e)

        return self.tuple
