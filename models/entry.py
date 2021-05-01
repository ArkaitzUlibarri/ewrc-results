import datetime


class Entry:

    def __init__(self, event_id, row):

        self.event_id = event_id

        self.car_number = None
        if row('td:not([class]):first').text()[1:]:
            self.car_number = row('td:not([class]):first').text()[1:]

        self.driver_id = row('td:not([class])').eq(1).find('a').attr('href').split('/')[2].split('-')[0]

        self.codriver_id = None
        if row('td:not([class]):last > a').attr('href'):
            self.codriver_id = row('td:not([class]):last').find('a').attr('href').split('/')[2].split('-')[0]

        self.car = row("td.bold").clone().find('span').remove().end().text()

        self.team = None
        if row("td.bold").find('span.r8'):
            self.team = row("td.bold").find('span.r8').text()

        self.plate = None
        if row("td.startlist-team").find("span.startlist-chassis"):
            self.plate = row("td.startlist-team").find("span.startlist-chassis").find('a').text().replace('[', '').replace(']', '')

        self.tyres = None
        if row("td.startlist-team").find("div.startlist-tyre-position"):
            self.tyres = row("td.startlist-team").find("div.startlist-tyre-position").find('img').attr('src').split('/')[3].split('.')[0].title()

        self.category = None
        if row("td:not(.startlist-m):not(.startlist-sections):last").text():
            self.category = row("td:not(.startlist-m):not(.startlist-sections):last").text()

        # self.championship = row("td.startlist-m").text()
        # self.sections = row("td.startlist-sections").text()

        self.set_timestamps()

    def set_timestamps(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.deleted_at = None

    def get_tuple(self):
        self.tuple = (self.event_id, self.car_number, self.driver_id, self.codriver_id, self.team, self.car, self.plate, self.tyres, self.category, self.created_at, self.updated_at, self. deleted_at)

        # print(self.tuple)

        return self.tuple
