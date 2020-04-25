import datetime

class Result():
	def __init__(self,driver_id,season,row):
		self.driver_id = driver_id
		self.season = int(season.text())

		self.event_id = row("div.profile-start-event").find('a').attr('href').split('/')[2].split('-')[0]

		self.codriver_id = None
		if(row("div.profile-start-codriver").find('a')):
			self.codriver_id = row("div.profile-start-codriver").find('a').attr('href').split('/')[2].split('-')[0]

		self.number = None
		if(row("div.profile-start-number").text()):
			self.number = row("div.profile-start-number").text().replace('#','')

		self.car = row("div.profile-start-car").clone().find('span.startlist-chassis').remove().end().find('span.r8').remove().end().find('a').remove().end().text().strip()
		
		self.plate = None
		if(row("div.profile-start-car").find('span.startlist-chassis')):
			self.plate = row("div.profile-start-car").find('span.startlist-chassis').text()

		self.team = None
		if(row("div.profile-start-car").find('span.r8')):
			self.team = row("div.profile-start-car").find('span.r8').text()

		self.chassis = None
		if(row("div.profile-start-car").find('span.c-grey')):
			self.chassis = row("div.profile-start-car").find('span.c-grey').text().replace('[chassis ','').replace(']','')

		self.category = None
		if(row("div.profile-start-cat").text()):
			self.category = row("div.profile-start-cat").text()

		if(row("div").hasClass("profile-start-oa")):
			result = row("div.profile-start-oa").text().replace('.','')  # Finishes
			class_result = [cr.text() for cr in row.items("div.profile-start-sub")]
		elif(row("div").hasClass("profile-start-ret")):
			result = row("div.profile-start-ret").text()  # Accidents
			class_result = []
		else:
			result = None
			class_result = []

		self.result = result
		self.class_result = class_result
		self.setTimestamps()

	def setTimestamps(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.deleted_at = None

	def getTuple(self):
		self.tuple = (self.event_id, self.driver_id, self.codriver_id, self.season, self.number, self.car, self.plate, self.team, self.chassis, self.category, self.result, self.created_at, self.updated_at, self. deleted_at)

		#print(self.tuple)

		return self.tuple
