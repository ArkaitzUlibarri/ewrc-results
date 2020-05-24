import os
import json
from config import app
from pptx import Presentation
from pptx.util import Cm
from database.stats import *

def createTable(data):
	rows,cols = len(data) + 1, len(data[0])
	left, top, width, height = Cm(1), Cm(4), Cm(rows * 24/14), Cm(cols * 11/6)
	return shapes.add_table(rows, cols, left, top, width, height).table

def writeTableHeadings(table,headings):
	for index,heading in enumerate(headings,start=0):
		table.cell(0, index).text = heading

def writeTableBody(table,data):
	for rowIndex,row in enumerate(data, start=1):
		for colIndex,cell in enumerate(row, start=0):
			table.cell(rowIndex, colIndex).text = str(cell)

# Clear console
os.system("cls")	

packageDir  = os.path.abspath(os.path.dirname(__file__))
db = os.path.join(packageDir,'database', app.database + '.db')

#Config
season = str(1993)

#Queries
scratchs = driversScratchs(db,season)
leaders = driversLeaders(db,season)
winners = driversWinners(db,season)
podiums = driversPodiums(db,season)
results = rallyWinners(db,season)

# TODO
#driverPointsSystem = driversChampionshipPointsSystem(db,season)
#fullResultsByDriver = fullResultsByDriver(db,season,1398)

#print(scratchs)
#print(json.loads(driverPointsSystem))

#create PPT
prs = Presentation()
layout = prs.slide_layouts[5]

#First Slide
slide = prs.slides.add_slide(layout)
shapes = slide.shapes
shapes.title.text = 'WORLD RALLY CHAMPIONSHIP ' + season

table = createTable(results)
writeTableHeadings(table,('#','Edición','Rallye','Ganador','Coche','Equipo'))
writeTableBody(table,results)

#Second slide
slide = prs.slides.add_slide(layout)
shapes = slide.shapes

table = createTable(winners)
writeTableHeadings(table,('Piloto','Victorias'))
writeTableBody(table,winners)

#save PPT
prs.save('WRC_' + season + '.pptx')
print('Finished ' + 'WRC_' + season + '.pptx' + ' export')
