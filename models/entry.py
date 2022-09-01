import datetime


def get_href_id(a_tag):
    return a_tag.attr('href').split('/')[2].split('-')[0]


def get_tyres(img_tag):
    return img_tag.attr('src').split('/')[5].split('.')[0].split('_')[0].upper()


class Entry:

    def __init__(self, event_id, row):

        delimiter = ','
        car_number = row('td:first')
        entry = row('td.startlist-entry')
        driver = entry.find('div.startlist-driver').eq(0)
        codriver = entry.find('div.startlist-driver').eq(1)
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

        self.car = car.clone().find('span').remove().end().text()

        self.team = None
        self.plate = None
        self.tyres = None
        self.category = None
        self.startlist_m = None
        self.championship = None

        if team:
            self.team = team.text()
        if plate:
            self.plate = plate.text()
        if tyres:
            self.tyres = get_tyres(tyres)
        if category.text():
            self.category = category.text()
        if startlist_m.text():
            self.startlist_m = startlist_m.text()
        if championship.html():
            self.championship = championship.text() 

        self.set_timestamps()

    def set_timestamps(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.deleted_at = None

    def get_tuple(self):
        self.tuple = (self.event_id, self.car_number, self.driver_id, self.codriver_id, self.team, self.car, self.plate,
                      self.tyres, self.category, self.startlist_m, self.championship,
                      self.created_at, self.updated_at, self.deleted_at)

        # print(self.tuple)

        return self.tuple
