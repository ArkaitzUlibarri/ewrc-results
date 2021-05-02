import datetime


def get_href_id(a_tag):
    return a_tag.attr('href').split('/')[2].split('-')[0]


def get_tyres(img_tag):
    return img_tag.attr('src').split('/')[5].split('.')[0].split('_')[0].upper()


class Entry:

    def __init__(self, event_id, row):

        self.event_id = event_id

        self.car_number = None
        if row('td:first').text()[1:]:
            self.car_number = row('td:first').text()[1:]

        entry = row('td.startlist-entry')
        self.driver_id = get_href_id(entry.find('div.startlist-driver').eq(0).find('a'))
        self.codriver_id = None
        if row('div.startlist-driver:last > a').attr('href'):
            self.codriver_id = get_href_id(entry.find('div.startlist-driver').eq(1).find('a'))

        self.car = row("td.font-weight-bold.lh-130").clone().find('span').remove().end().text()

        self.team = None
        if row("td.font-weight-bold.lh-130").find('span'):
            self.team = row("td.font-weight-bold.lh-130").find('span').text()

        self.plate = None
        if row("td.startlist-team > a"):
            self.plate = row("td.startlist-team").find('a').text()

        self.tyres = None
        if row("td.startlist-team > img"):
            self.tyres = get_tyres(row("td.startlist-team").find('img'))

        self.category = None
        if row("td.fs-091:first").text():
            self.category = row("td.fs-091:first").text()

        # self.championship = row("td.entry-sct").text()

        self.set_timestamps()

    def set_timestamps(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.deleted_at = None

    def get_tuple(self):
        self.tuple = (self.event_id, self.car_number, self.driver_id, self.codriver_id, self.team, self.car, self.plate, self.tyres, self.category, self.created_at, self.updated_at, self. deleted_at)

        # print(self.tuple)

        return self.tuple
