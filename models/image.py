import datetime


class Image:

	def __init__(self, event_id, image_id, base_url):
		self.id = image_id
		self.event_id = event_id
		self.url = base_url + '/' + 'image' + '/' + self.id + '/'
		self.set_timestamps()

	def set_timestamps(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.deleted_at = None

	def get_tuple(self):
		self.tuple = (self.id, self.event_id, self.created_at, self.updated_at, self. deleted_at)

		# print(self.tuple)

		return self.tuple
