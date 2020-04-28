import datetime

class Image():

	def __init__(self,event_id, image_id):
		self.id = image_id
		self.event_id = event_id
		self.setTimestamps()

	def setTimestamps(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.deleted_at = None

	def getTuple(self):
		self.tuple = (self.id, self.event_id, self.created_at, self.updated_at, self. deleted_at)

		#print(self.tuple)

		return self.tuple
