class Driver():

	def __init__(self,doc,id):
		self.id = id
		self.getNames(doc)
		self.getNationality(doc)
		self.getDates(doc)

	def getNames(self, doc):
		self.fullname = doc(".profile > h1").text()
		header = [h.text() for h in doc.items("div.profile-header-data > table > tr > td > strong")]
		self.lastname = header[0]
		self.name = header[1]

	def getDates(self, doc):
		self.birthdate = None
		self.deathdate = None
		dates = [d.text().replace(". ","-") for d in doc.items("div.profile-header-data > table > tr > td > b")]
		for date in dates:
			if(self.hasNumbers(date)):
				if(self.birthdate == None):
					self.birthdate = date
				elif(self.deathdate == None):
					self.deathdate = date

	def getNationality(self, doc):
		nationality = [n.text() for n in doc.items("div.profile-header-flag > div.profile-header-nat")]
		if len(nationality) == 2:
			self.nationality = nationality[1]
		else:
			self.nationality = nationality[0]

	def hasNumbers(self,inputString):
		return any(char.isdigit() for char in inputString)

	def getTuple(self):
		self.tuple = (self.id, self.fullname, self.name, self.lastname, self.birthdate, self.deathdate, self.nationality)

		#print(self.tuple)

		return self.tuple
