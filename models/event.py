import datetime

class Event():

	def __init__(self,season,item,index):

		self.get_event_id(item)
		self.season = str(season)
		self.season_event_id = index
		self.get_event_name(item)
		self.get_event_surface(item)
		self.get_event_info(item)
		self.set_timestamps()

	def is_cancelled(self,item):
		for div in item.items("div"):
			if div.hasClass("widget-canceled"):
				return True
		return False

	def get_event_info(self,item):
		if not self.is_cancelled(item):
			event_info = item(".event-info").text().split(u'\u2022')

			self.dates = event_info[0].strip()
			entries_info = event_info[1].split('-')[1].split('/')

			self.entries = entries_info[0].strip()
			self.finish = entries_info[1].strip()
		else:
			self.dates = None
			self.entries = None
			self.finish = None

	def get_event_id(self,item):
		self.event_id = item(".season-event-name a").attr('href').split('/')[2].split('-')[0]

	def get_event_name(self,item):
		event_name = item(".season-event-name").text().strip()

		self.edition = None
		self.name = event_name

		if "." in event_name:
			self.edition = event_name.split('.')[0]
			self.name = event_name.split('.')[1]

	def get_event_surface(self,item):
		info = item(".event-info").text()

		self.asphalt = "asphalt" in info or "tarmac" in info
		self.gravel = "gravel" in info
		self.snow = "snow" in info
		self.ice = "ice" in info

	def set_timestamps(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.deleted_at = None
		
	def get_tuple(self):
		self.tuple = (self.event_id, self.season, self.season_event_id, self.edition, self.name, self.asphalt, self.gravel, self.snow, self.ice, self.dates, self.entries, self.finish, self.created_at, self.updated_at, self. deleted_at)

		#print(self.tuple)

		return self.tuple
