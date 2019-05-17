class Result():
	def __init__(self,driver,season,tr):
		self.driver = driver
		self.codriver = tr("div.profile-start-codriver").text()
		self.season = int(season.text())
		self.event_id = tr("div.profile-start-event > a").attr('href').split('/')[2].split('-')[0]
		self.number = tr("div.profile-start-number").text().replace('#','')
		self.plate = tr("div.profile-start-car > span.startlist-chassis").text()
		self.team = tr("div.profile-start-car > span.r8").text()
		self.car = tr("div.profile-start-car").remove('span.startlist-chassis').remove('span.r8').text()
		self.category = tr("div.profile-start-cat").text()

		if(tr("div").hasClass("profile-start-oa")):
			result = tr("div.profile-start-oa").text().replace('.','')	# Finishes
			class_result = [cr.text() for cr in tr.items("div.profile-start-sub")]
		elif(tr("div").hasClass("profile-start-ret")):
			result = tr("div.profile-start-ret").text()	# Accidents
			class_result = []
		else:
			result = '?'
			class_result = []

		self.result = result
		self.class_result = class_result