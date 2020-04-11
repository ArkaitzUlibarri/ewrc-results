class Event():

	def __init__(self,season,item,index):

		self.getEventId(item)
		self.season = str(season)
		self.season_event_id = index
		self.getEventName(item)
		self.getEventSurface(item)
		self.getEventInfo(item)
		#table = item(".tablefull") #TODO

	def isCanceled(self,item):
		for div in item.items("div"):
			if div.hasClass("widget-canceled"):
				return True
		return False

	def getEventInfo(self,item):
		if not self.isCanceled(item):
			event_info = item(".event-info").text().split(u'\u2022')

			self.dates = event_info[0]
			entries_info = event_info[1].split('-')[1].split('/')

			self.entries = entries_info[0]
			self.finish = entries_info[1]
		else:
			self.dates = None
			self.entries = None
			self.finish = None

	def getEventId(self,item):
		self.event_id = item(".season-event-name a").attr('href').split('/')[2].split('-')[0]

	def getEventName(self,item):
		event_name = item(".season-event-name").text()

		self.edition = None
		self.name = event_name

		if "." in event_name:
			self.edition = event_name.split('.')[0]
			self.name = event_name.split('.')[1]

	def getEventSurface(self,item):
		info = item(".event-info").text()

		self.asphalt = "asphalt" in info or "tarmac" in info
		self.gravel = "gravel" in info
		self.snow = "snow" in info
		self.ice = "ice" in info

	def printData(self):
		print(self.event_id + " " + self.season + " " + str(self.season_event_id) + " " + self.rally_name)