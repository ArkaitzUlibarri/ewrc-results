import os
import sys
import requests
import sqlite3
import shutil
from pyquery import PyQuery as pq
from models.image import Image


def insert_event_photos(base_url, db_path, event_ids_dict):
	current_file = os.path.basename(__file__)
	current_file_name = os.path.splitext(current_file)[0]

	for key in event_ids_dict:
		for event_id in event_ids_dict[key]:

			url = base_url + "/" + current_file_name + "/" + str(event_id) + "/"

			try:
				print(url)
				response = requests.get(url)
			except requests.exceptions.RequestException as e:
				print(e)
				sys.exit(1)

			if response.status_code == 200:

				doc = pq(response.text)

				try:
					db = sqlite3.connect(db_path)
					cursor = db.cursor()

					# Event Photos
					for photo in doc("div.foto-image").items():
						image_id = photo.find('a').attr('href').split('/')[1]
						image = Image(event_id, image_id, base_url)

						# Image URL
						image_response = requests.get(image.url)
						if image_response.status_code == 200:
							image_url = pq(image_response.text).find('img').attr('src')
							extension = image_url.rsplit('.')[-1]

							image_content = requests.get(image_url, stream=True)

							# Create target Directory if don't exist
							if not os.path.exists(os.path.join('storage', str(event_id))):
								os.mkdir(os.path.join('storage', str(event_id)))

							storage_path = os.path.join('storage', str(event_id), image_id + '.' + extension)
					
							with open(storage_path, 'wb+') as out_file:
								shutil.copyfileobj(image_content.raw, out_file)
							del image_content

						db.execute('''INSERT INTO images 
                        (id,event_id,created_at,updated_at,deleted_at) 
                        VALUES (?,?,?,?,?)''', image.get_tuple());

					db.commit()

				except Exception as e:
					db.rollback()	
					raise e
				finally:
					db.close()
