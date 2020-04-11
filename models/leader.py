class Leader():

	def __init__(self,tr,event_id, driver_id):
		self.event_id = event_id
		self.stage_number = tr("td:first > a").text()
		self.stage_name = tr("td.stats-stage2 > a").text()
		self.driver_id = driver_id

	def getTuple(self):
		self.tuple = (self.event_id, self.stage_number, self.stage_name, self.driver_id)

		#print(self.tuple)

		return self.tuple
