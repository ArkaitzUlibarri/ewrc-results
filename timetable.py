import os
import sys
import requests
import sqlite3
from pyquery import PyQuery as pq

currentfile = os.path.basename(__file__)
currentfilename = os.path.splitext(currentfile)[0]

os.system("cls")	# Clear console

url = "https://www.ewrc-results.com/"+ currentfilename + "/"+ "53052-rally-sweden-2019/"

try:
	print(url)
	response = requests.get(url)
except requests.exceptions.RequestException as e:
	print(e)
	sys.exit(1)

if response.status_code == 200:

	doc = pq(response.text)

	timetable = doc('.timetable')

	for tr in timetable('tr').items():
		if tr.hasClass('servis'):
			service_name = tr('td').eq(1).text()
			date = tr('td.td_right').text()
			hour = tr('td:last').text()
			print(service_name + " " + date + " " + hour)
		else:
			number = tr('td:first > a').text()
			stage_name = tr('td > a').eq(1).text()
			#stage_id = tr('td > a').eq(1).attr('href')
			distance = tr('td.td_right.nwrap').text()
			date = tr('td.td_right').not_('.nwrap').text()
			gmt = tr('td:last > span.timetable-gmt').text()
			tr('td:last > span.timetable-gmt').remove()
			hour = tr('td:last').text()
			#print(number + " " + stage_name + " " + distance + " " + date + " " + hour + " " + gmt)