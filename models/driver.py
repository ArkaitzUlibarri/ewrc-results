import datetime


def has_numbers(input_string):
	return any(char.isdigit() for char in input_string)


class Driver:

	def __init__(self, doc, id):
		self.id = id
		self.fullname = doc(".profile > h4").text()
		header = [h.text() for h in doc.items("div.profile-header-data").find('td.font-weight-bold')]
		self.lastname = header[0]
		self.name = header[1]
		self.nationality = doc("div.profile-header-data").find('img.flag-s').parent('td').text().strip()
		self.birthdate = None
		self.deathdate = None
		if has_numbers(header[2].replace(". ", "-")):
			self.birthdate = header[2].replace(". ", "-")
		if doc("div.profile-header-data").find('i.fa-cross'):
			self.deathdate = header[3].replace(". ", "-")
		self.get_dates(doc)
		self.set_timestamps()

	def get_dates(self, doc):
		self.birthdate = None
		self.deathdate = None
		dates = [d.text().replace(". ", "-") for d in doc.items("div.profile-header-data > table > tr > td > b")]
		for date in dates:
			if has_numbers(date):
				if self.birthdate is None:
					self.birthdate = date
				elif self.deathdate is None:
					self.deathdate = date

	def set_timestamps(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.deleted_at = None

	def get_tuple(self):
		self.tuple = (self.id, self.fullname, self.name, self.lastname, self.birthdate, self.deathdate, self.nationality, self.created_at, self.updated_at, self. deleted_at)

		# print(self.tuple)

		return self.tuple
