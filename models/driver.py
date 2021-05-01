import datetime


class Driver:

	def __init__(self, doc, id):
		self.id = id
		self.get_names(doc)
		self.get_nationality(doc)
		self.get_dates(doc)
		self.set_timestamps()

	def get_names(self, doc):
		self.fullname = doc(".profile > h1").text()
		header = [h.text() for h in doc.items("div.profile-header-data > table > tr > td > strong")]
		self.lastname = header[0]
		self.name = header[1]

	def get_dates(self, doc):
		self.birthdate = None
		self.deathdate = None
		dates = [d.text().replace(". ", "-") for d in doc.items("div.profile-header-data > table > tr > td > b")]
		for date in dates:
			if self.has_numbers(date):
				if self.birthdate is None:
					self.birthdate = date
				elif self.deathdate is None:
					self.deathdate = date

	def get_nationality(self, doc):
		nationality = [n.text() for n in doc.items("div.profile-header-flag > div.profile-header-nat")]
		if len(nationality) == 2:
			self.nationality = nationality[1]
		else:
			self.nationality = nationality[0]

	def has_numbers(self, input_string):
		return any(char.isdigit() for char in input_string)

	def set_timestamps(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.deleted_at = None

	def get_tuple(self):
		self.tuple = (self.id, self.fullname, self.name, self.lastname, self.birthdate, self.deathdate, self.nationality, self.created_at, self.updated_at, self. deleted_at)

		# print(self.tuple)

		return self.tuple
