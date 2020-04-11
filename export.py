import os
import config
from pptx import Presentation
from pptx.util import Cm
from helpers.db_helpers import rallyWinners,driversStats,driversResults

os.system("cls")	# Clear console

#Config
season = str(1993)
databaseName = config.database + '.db'

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

#Queries
scratchs = driversStats(databaseName,season,'scratchs')
leaders = driversStats(databaseName,season,'leaders')
winners = driversResults(databaseName,season,'winners')
podiums = driversResults(databaseName,season,'podiums')
results = rallyWinners(databaseName,season)

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