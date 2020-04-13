class Driver():

	def __init__(self,doc,id):
		self.id = id
		self.fullname = doc(".profile > h1").text()

		header = [h.text() for h in doc.items("div.profile-header-data > table > tr > td > strong")]
		self.lastname = header[0]
		self.name = header[1]

		nationality = [n.text() for n in doc.items("div.profile-header-flag > div.profile-header-nat")]
		if len(nationality) == 2:
			self.nationality = nationality[1]
		else:
			self.nationality = nationality[0]

		dates = [d.text().replace(". ","-") for d in doc.items("div.profile-header-data > table > tr > td > b")]
		self.birthdate = dates[0]
		self.deathdate = None
		if len(dates) == 2:
			self.deathdate = dates[1]

	def getTuple(self):
		self.tuple = (self.id, self.fullname, self.name, self.lastname, self.birthdate, self.deathdate, self.nationality)

		#print(self.tuple)

		return self.tuple
