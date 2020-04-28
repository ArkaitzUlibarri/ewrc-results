import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq
from models.image import Image

def insertEventPhotos(base_url, dbPath, event_ids_dict):
	currentfile = os.path.basename(__file__)
	currentfilename = os.path.splitext(currentfile)[0]

	for key in event_ids_dict:
		for event_id in event_ids_dict[key]:

			url = base_url + "/" + currentfilename + "/" + str(event_id) + "/"

			try:
				print(url)
				response = requests.get(url)
			except requests.exceptions.RequestException as e:
				print(e)
				sys.exit(1)

			if response.status_code == 200:

				doc = pq(response.text)

				try:
					db = sqlite3.connect(dbPath)
					cursor = db.cursor()

					# Event Photos
					for photo in doc("div.foto-image").items():
						image_id = photo.find('a').attr('href').split('/')[1]
						image = Image(event_id, image_id)
						db.execute('''INSERT INTO images 
                        (id,event_id,created_at,updated_at,deleted_at) 
                        VALUES (?,?,?,?,?)''', image.getTuple());

					db.commit()

				except Exception as e:
					db.rollback()	
					raise e
				finally:
					db.close()
