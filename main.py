import os
from config import app
from database.migrations import events
from database.migrations import drivers
from database.migrations import codrivers
from database.migrations import scratchs
from database.migrations import leaders
from database.migrations import entries
from database.migrations import images
from database.migrations import points
from database.migrations import nationalities
from database.migrations import championships
from database.seeds import seeder
from services import main_service
from services import nationality_service
from services import championship_service
from pages import season as season_page
from pages import entries as entry_page
from pages import final as result_page
from pages import eventstats as event_stats_page
from pages import photo as event_photos_page
from pages import profile as profile_page
from pages import coprofile as coprofile_page
from pages import timetable as event_timetable_page

# Clear console
os.system("cls")

print('---------------')
print('Execution Start')
print('---------------')

# Migrations
events.migrate()
drivers.migrate()
codrivers.migrate()
scratchs.migrate()
leaders.migrate()
entries.migrate()
images.migrate()
points.migrate()
nationalities.migrate()
championships.migrate()

# Seeders
seeder.championship_points()

# Season Options
season_list = season_page.get_seasons()
start_season = season_list[-1]

for item in season_list:
    season_page.insert_nationalities(item)

nationality_list = nationality_service.select_nationalities()

for item in season_list:
    for index, row in enumerate(nationality_list, start=1):
        season_page.insert_championships(item, row['id'])

# Events
season_page.insert_events( start_season, "1-wrc")

# Select Events Data
championship_list = championship_service.select_championships()
event_ids_dict = main_service.select_events(start_season)

# Event Photos
event_photos_page.insert_event_photos(event_ids_dict)

# Event Stats
event_stats_page.insert_event_stats(event_ids_dict)

# Event Timetable
event_timetable_page.get_timetable(event_ids_dict)

# Entries
entry_page.insert_entries(event_ids_dict, championship_list)

# Results
events_list = main_service.select_events_without_results()
result_page.insert_results(events_list)

# Select Entries Data
driver_list = main_service.select_drivers()
codriver_list = main_service.select_codrivers()

# Drivers
profile_page.insert_drivers(driver_list, app.category)

# Codrivers
coprofile_page.insert_codrivers(codriver_list, app.category)

print('----------------')
print('Execution Finish')
print('----------------')