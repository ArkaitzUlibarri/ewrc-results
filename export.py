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


def write_table_headings(ppt_table, headings):
    for index, heading in enumerate(headings, start=0):
        ppt_table.cell(0, index).text = heading


def write_table_body(ppt_table, data):
    for row_index, row in enumerate(data, start=1):
        for col_index, cell in enumerate(row, start=0):
            ppt_table.cell(row_index, col_index).text = str(cell)


# Clear console
os.system("cls")

package_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(package_dir, 'database', app.database + '.db')

# Config
season = str(1993)

# Queries
scratchs = drivers_scratchs(db_path, season)
leaders = drivers_leaders(db_path, season)
win_stats = drivers_winners(db_path, season)
podium_stats = drivers_podiums(db_path, season)
season_winners = rally_winners(db_path, season)

# Driver Points
driverPointsSystem = drivers_championship_points_system(db_path, season)
full_results_by_driver = full_results_by_driver(db_path, season, 1398)

# print(scratchs)
print(json.loads(driverPointsSystem))

# create PPT
prs = Presentation()
layout = prs.slide_layouts[5]

# First Slide - Season Winners
slide = prs.slides.add_slide(layout)
shapes = slide.shapes
shapes.title.text = 'WORLD RALLY CHAMPIONSHIP ' + season

table = create_table(season_winners)
write_table_headings(table, ('#', 'Edition', 'Rally', 'Winner', 'Car', 'Team'))
write_table_body(table, season_winners)

# Second slide - Win stats
slide = prs.slides.add_slide(layout)
shapes = slide.shapes
shapes.title.text = 'STATS ' + season

table = create_table(win_stats)
write_table_headings(table, ('Driver', 'Wins'))
write_table_body(table, win_stats)

# Third slide - Podium stats
slide = prs.slides.add_slide(layout)
shapes = slide.shapes
shapes.title.text = 'STATS ' + season

table = create_table(podium_stats)
write_table_headings(table, ('Driver', 'Podiums'))
write_table_body(table, podium_stats)

# Fourth slide - Scratchs stats
slide = prs.slides.add_slide(layout)
shapes = slide.shapes
shapes.title.text = 'STATS ' + season

table = create_table(scratchs)
write_table_headings(table, ('Driver', 'Scratchs'))
write_table_body(table, scratchs)

# Fifth slide - Leaders stats
slide = prs.slides.add_slide(layout)
shapes = slide.shapes
shapes.title.text = 'STATS ' + season

table = create_table(scratchs)
write_table_headings(table, ('Driver', 'Scratchs'))
write_table_body(table, scratchs)

# save PPT
package_dir = os.path.abspath(os.path.dirname(__file__))
export_folder = os.path.join(package_dir, 'storage', 'exports')
if not os.path.exists(export_folder):
    os.makedirs(export_folder)

export_path = os.path.join(package_dir, 'storage', 'exports', 'WRC_' + season + '.pptx')
prs.save(export_path)

print('Finished ' + export_path + ' export')
