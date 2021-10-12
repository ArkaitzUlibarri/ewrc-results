import datetime


def get_href_id(a_tag):
    return a_tag.attr('href').split('/')[2].split('-')[0]


class Result:
    def __init__(self, driver_id, row):

        event = row("div.profile-start-event")
        codriver = row("div.profile-start-codriver")
        car_number = row("div.profile-start-number")
        car = row("div.profile-start-car")
        team = car.find('span.font-weight-normal')
        car_info = car.find('span.startlist-chassis')
        category = row("div.profile-start-cat")

        self.car_number = None
        self.driver_id = driver_id
        self.event_id = get_href_id(event.find('a'))
        self.codriver_id = None
        self.team = None
        self.plate = None
        self.category = None
        if codriver.find('a'):
            self.codriver_id = get_href_id(codriver.find('a'))
        if car_number.text():
            self.car_number = car_number.text().replace('#', '')
        self.car = car.clone().find('span').remove().end().text()
        if team:
            self.team = team.text()
        if car_info:
            self.plate = car_info.find('a:first').text()
        if category.text():
            self.category = category.text()

        result = None
        if row("div").hasClass("profile-start-oa"):
            result = row("div.profile-start-oa").clone().find('span').remove().end().text().replace('.', '')  # Finishes
        elif row("div").hasClass("profile-start-ret"):
            result = row("div.profile-start-ret").text()  # Accidents

        self.result = result
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
            self.category,
            self.result,
            self.created_at,
            self.updated_at,
            self.deleted_at
        )

        # print(self.tuple)

        return self.tuple
