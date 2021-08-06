import datetime


def get_href_id(a_tag):
    return a_tag.attr('href').split('/')[2].split('-')[0]


def get_chassis(text):
    return text.replace('[chassis ', '').replace(']', '')


class Result:
    def __init__(self, driver_id, season, row):

        event = row("div.profile-start-event")
        codriver = row("div.profile-start-codriver")
        number = row("div.profile-start-number")
        car = row("div.profile-start-car")
        team = car.find('span.font-weight-normal')
        car_info = car.find('span.startlist-chassis')
        category = row("div.profile-start-cat")

        self.driver_id = driver_id
        self.season = int(season.text())
        self.event_id = get_href_id(event.find('a'))
        self.codriver_id = None
        self.number = None
        self.team = None
        self.plate = None
        self.chassis = None
        self.category = None
        if codriver.find('a'):
            self.codriver_id = get_href_id(codriver.find('a'))
        if number.text():
            self.number = number.text().replace('#', '')
        self.car = car.clone().find('span').remove().end().text()
        if team:
            self.team = team.text()
        if car_info:
            self.plate = car_info.find('a:first').text()
            if len(car_info.find('a')) == 2:
                self.chassis = get_chassis(car_info.find('a:last').text())
        if category.text():
            self.category = category.text()

        result = None
        class_result = []
        if row("div").hasClass("profile-start-oa"):
            result = row("div.profile-start-oa").clone().find('span').remove().end().text().replace('.', '')  # Finishes
            # FIXME
            # class_result = [cr.text() for cr in row.items("div.profile-start-sub")]
        elif row("div").hasClass("profile-start-ret"):
            result = row("div.profile-start-ret").text()  # Accidents
            class_result = []

        self.result = result
        self.class_result = class_result
        self.set_timestamps()

    def set_timestamps(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.deleted_at = None

    def get_tuple(self):
        self.tuple = (
            self.event_id,
            self.driver_id,
            self.codriver_id,
            self.season,
            self.number,
            self.car,
            self.plate,
            self.team,
            self.chassis,
            self.category,
            self.result,
            self.created_at,
            self.updated_at,
            self.deleted_at
        )

        # print(self.tuple)

        return self.tuple
