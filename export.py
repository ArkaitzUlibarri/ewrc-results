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


def get_driver_season_stats(results, points_dict):
    starts = 0
    wins = 0
    podiums = 0
    top5 = 0
    dnfs = 0
    total_points = 0
    for row_index, row in enumerate(results, start=1):
        starts += 1
        points = '0'
        result = row['result']

        if not result.isnumeric():
            dnfs += 1
        else:
            if int(result) == 1:
                wins += 1
            if int(result) <= 3:
                podiums += 1
            if int(result) <= 5:
                top5 += 1
            if result in points_dict:
                points = points_dict[result]

        total_points += int(points)
        print("Result: " + result + ", Points: " + points)
    print("Starts: " + str(starts)
          + ", Wins: " + str(wins)
          + ", Podiums: " + str(podiums)
          + ", TOP5: " + str(top5)
          + ", DNFs: " + str(dnfs)
          + ", Points: " + str(total_points))


# Clear console
os.system("cls")

package_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(package_dir, 'database', app.database + '.db')

# Config
season = str(1997)

# Queries
scratchs = drivers_scratchs(db_path, season)
leaders = drivers_leaders(db_path, season)
win_stats = drivers_winners(db_path, season)
podium_stats = drivers_podiums(db_path, season)
season_winners = rally_winners(db_path, season)

# Driver Points
# TODO: Pilotos en el podio durante el año + pilotos de marcas oficiales
driverPointsSystem = drivers_championship_points_system(db_path, season, 'drivers')
driver_points_system_dict = json.loads(driverPointsSystem)
print(driver_points_system_dict)
full_results_by_driver = full_results_by_driver(db_path, season, 848)

# get_driver_season_stats(full_results_by_driver, driver_points_system_dict)

# create PPT
# prs = Presentation()
# layout = prs.slide_layouts[5]

# # First Slide - Season Winners
# slide = prs.slides.add_slide(layout)
# shapes = slide.shapes
# shapes.title.text = 'WORLD RALLY CHAMPIONSHIP ' + season
#
# table = create_table(season_winners)
# write_table_headings(table, ('#', 'Edition', 'Rally', 'Winner', 'Car', 'Team'))
# write_table_body(table, season_winners)
#
# # Second slide - Win stats
# slide = prs.slides.add_slide(layout)
# shapes = slide.shapes
# shapes.title.text = 'STATS ' + season
#
# table = create_table(win_stats)
# write_table_headings(table, ('Driver', 'Wins'))
# write_table_body(table, win_stats)
#
# # Third slide - Podium stats
# slide = prs.slides.add_slide(layout)
# shapes = slide.shapes
# shapes.title.text = 'STATS ' + season
#
# table = create_table(podium_stats)
# write_table_headings(table, ('Driver', 'Podiums'))
# write_table_body(table, podium_stats)
#
# # Fourth slide - Scratchs stats
# slide = prs.slides.add_slide(layout)
# shapes = slide.shapes
# shapes.title.text = 'STATS ' + season
#
# table = create_table(scratchs)
# write_table_headings(table, ('Driver', 'Scratchs'))
# write_table_body(table, scratchs)
#
# # Fifth slide - Leaders stats
# slide = prs.slides.add_slide(layout)
# shapes = slide.shapes
# shapes.title.text = 'STATS ' + season
#
# table = create_table(scratchs)
# write_table_headings(table, ('Driver', 'Scratchs'))
# write_table_body(table, scratchs)

# save PPT
# package_dir = os.path.abspath(os.path.dirname(__file__))
# export_folder = os.path.join(package_dir, 'storage', 'exports')
# if not os.path.exists(export_folder):
#     os.makedirs(export_folder)
#
# export_path = os.path.join(package_dir, 'storage', 'exports', 'WRC_' + season + '.pptx')
# prs.save(export_path)

# print('Finished ' + export_path + ' export')
