import os
import json
from config import app
from pptx import Presentation
from pptx.util import Cm
from database.stats import *


def create_table(data):
    rows, cols = len(data) + 1, len(data[0])
    left, top, width, height = Cm(1), Cm(4), Cm(rows * 24 / 14), Cm(cols * 11 / 6)
    return shapes.add_table(rows, cols, left, top, width, height).table


def write_table_headings(table, headings):
    for index, heading in enumerate(headings, start=0):
        table.cell(0, index).text = heading


def write_table_body(table, data):
    for row_index, row in enumerate(data, start=1):
        for col_index, cell in enumerate(row, start=0):
            table.cell(row_index, col_index).text = str(cell)


# Clear console
os.system("cls")

package_dir = os.path.abspath(os.path.dirname(__file__))
db = os.path.join(package_dir, 'database', app.database + '.db')

# Config
season = str(1993)

# Queries
scratchs = drivers_scratchs(db, season)
leaders = drivers_leaders(db, season)
winners = drivers_winners(db, season)
podiums = drivers_podiums(db, season)
results = rally_winners(db, season)

# TODO
# driverPointsSystem = drivers_championship_points_system(db,season)
# full_results_by_driver = full_results_by_driver(db,season,1398)

# print(scratchs)
# print(json.loads(driverPointsSystem))

# create PPT
prs = Presentation()
layout = prs.slide_layouts[5]

# First Slide
slide = prs.slides.add_slide(layout)
shapes = slide.shapes
shapes.title.text = 'WORLD RALLY CHAMPIONSHIP ' + season

table = create_table(results)
write_table_headings(table, ('#', 'Edition', 'Rally', 'Winner', 'Car', 'Team'))
write_table_body(table, results)

# Second slide
slide = prs.slides.add_slide(layout)
shapes = slide.shapes

table = create_table(winners)
write_table_headings(table, ('Driver', 'Wins'))
write_table_body(table, winners)

# save PPT
prs.save('WRC_' + season + '.pptx')
print('Finished ' + 'WRC_' + season + '.pptx' + ' export')
