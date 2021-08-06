import datetime


def format_date(date):
    return date.replace(". ", "-")


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


class Driver:

    def __init__(self, doc, driver_id):
        self.id = driver_id
        self.fullname = doc(".profile > h4").text()
        header_data = doc("div.profile-header-data")
        headers = header_data.find('td.font-weight-bold').items()
        header = [h.text() for h in headers]
        self.lastname = header[0]
        self.name = header[1]
        self.nationality = header_data.find('img.flag-s').parent('td').text().strip()
        self.birthdate = None
        self.deathdate = None
        if has_numbers(format_date(header[2])):
            self.birthdate = format_date(header[2])
        if header_data.find('i.fa-cross'):
            self.deathdate = format_date(header[3])
        self.set_timestamps()

    def set_timestamps(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.deleted_at = None

    def get_tuple(self):
        self.tuple = (
            self.id,
            self.fullname,
            self.name,
            self.lastname,
            self.birthdate,
            self.deathdate,
            self.nationality,
            self.created_at,
            self.updated_at,
            self.deleted_at
        )

        print(self.tuple)

        return self.tuple
