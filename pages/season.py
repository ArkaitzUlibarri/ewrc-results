import os
import sys
import requests
import sqlite3
import datetime
from pyquery import PyQuery as pq
from models.event import Event


def get_seasons(base_url):
	current_file = os.path.basename(__file__)
	current_file_name = os.path.splitext(current_file)[0]

	url = base_url + "/" + current_file_name + "/"

	try:
		print(url)
		response = requests.get(url)
	except requests.exceptions.RequestException as e:
		print(e)
		sys.exit(1)

	if response.status_code == 200:

		doc = pq(response.text)

		output = list()

		try:
			header = doc('.justify-content-start').not_('.season-nat').not_('.season-sct').not_('.header-flags')
			badges = header.find('a.badge').items()

			for index, badge in enumerate(badges, start=1):
				season = badge.attr('href').split('/')[2]
				output.append(season)

			return output

		except Exception as e:
			print(str(e))
			return list()


def get_nationalities(base_url, season):
	current_file = os.path.basename(__file__)
	current_file_name = os.path.splitext(current_file)[0]

	url = base_url + "/" + current_file_name + "/"+ str(season) + "/"

	try:
		print(url)
		response = requests.get(url)
	except requests.exceptions.RequestException as e:
		print(e)
		sys.exit(1)

	if response.status_code == 200:

		doc = pq(response.text)

		output = list()

		try:
			header = doc('.justify-content-start.season-nat')
			badges = header.find('a.badge').items()

			for index, badge in enumerate(badges, start=1):
				code = badge.attr('href').split('/')[3].replace('?nat=','')
				nationality = badge.text()
				output.append({'code': code, 'nationality': nationality})

			return output

		except Exception as e:
			print(str(e))
			return list()


def get_championships(base_url, season, nationality_code):
	current_file = os.path.basename(__file__)
	current_file_name = os.path.splitext(current_file)[0]

	url = base_url + "/" + current_file_name + "/"+ str(season) + "/" + '?nat=' + nationality_code

	try:
		print(url)
		response = requests.get(url)
	except requests.exceptions.RequestException as e:
		print(e)
		sys.exit(1)

	if response.status_code == 200:

		doc = pq(response.text)

		output = list()

		try:
			header = doc('.justify-content-start.season-sct')
			badges = header.find('.season-sct-item').find('a.badge').items()

			for index, badge in enumerate(badges, start=1):
				code = badge.attr('href').split('/')[3]
				championship = badge.text()
				output.append({'code': code, 'championship': championship})

			return output

		except Exception as e:
			print(str(e))
			return list()
			

def insert_events(base_url, db_path, db_name, start_season):
	current_file = os.path.basename(__file__)
	current_file_name = os.path.splitext(current_file)[0]

	for season in range(start_season, datetime.datetime.now().year + 1):

		url = base_url + "/" + current_file_name + "/" + str(season) + "/" + db_name + "/"

		try:
			print(url)
			response = requests.get(url)
		except requests.exceptions.RequestException as e:
			print(e)
			sys.exit(1)

		if response.status_code == 200:

			doc = pq(response.text)

			connection = sqlite3.connect(db_path)

			try:

				# Events
				events = doc.items(".season-event")
				for index, event in enumerate(events, start=1):
					rally = Event(season, event, index)
					connection.execute('''REPLACE INTO events 
					(id,season,season_event_id,edition,name,asphalt,gravel,snow,ice,dates,entries,finish,created_at,updated_at,deleted_at) 
					VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', rally.get_tuple())

				connection.commit()

			except Exception as e:
				connection.rollback()
				raise e
			finally:
				connection.close()
