class Scratch():

	def __init__(self,tr,event_id, driver_id):
		self.event_id = event_id
		self.stage_number = tr("td:first > a").text()
		self.stage_name = tr("td.stats-stage1 > a").text()
		self.driver_id = driver_id
		self.setTimestamps()

	def setTimestamps(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.deleted_at = None

	def getTuple(self):
		self.tuple = (self.event_id, self.stage_number, self.stage_name, self.driver_id, self.created_at, self.updated_at, self. deleted_at)

		#print(self.tuple)

		return self.tuple
