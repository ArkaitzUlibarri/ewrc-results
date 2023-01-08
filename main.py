import os

from config import app
from database.migrations import championship_migration
from database.migrations import codrivers_migration
from database.migrations import drivers_migration
from database.migrations import entries_migration
from database.migrations import events_migration
from database.migrations import images_migration
from database.migrations import leaders_migration
from database.migrations import nationalities_migration
from database.migrations import points_migration
from database.migrations import scratchs_migration
from database.seeds import points_seeder
from pages import coprofile as coprofile_page
from pages import entries as entry_page
from pages import eventstats as event_stats_page
from pages import final as result_page
from pages import photo as event_photos_page
from pages import profile as profile_page
from pages import season as season_page
from pages import timetable as event_timetable_page
from services import championship_service
from services import entry_service
from services import event_service
from services import nationality_service

# Clear console
os.system("cls")

print('Execution Start'.center(50, '-'))

print('Migrations Start'.center(50, '-'))

events_migration.up()
drivers_migration.up()
codrivers_migration.up()
scratchs_migration.up()
leaders_migration.up()
entries_migration.up()
images_migration.up()
points_migration.up()
nationalities_migration.up()
championship_migration.up()

print('Migrations End'.center(50, '-'))

print('Seeders Start'.center(50, '-'))

points_seeder.run()

print('Seeders End'.center(50, '-'))

# Season Options
season_list = season_page.get_seasons()
start_season = season_list[-1]

# # Insert nationalities
# for item in season_list:
#     season_page.insert_nationalities(item)

# # Select nationalities
# nationality_list = nationality_service.select_nationalities()

# # Insert championships
# for item in season_list:
#     for index, row in enumerate(nationality_list, start=1):
#         season_page.insert_championships(item, row['id'])

# Insert Events
season_page.insert_events(start_season, app.EVENTS_TYPE)

# Select Events Data
championship_list = championship_service.select_championships()
event_ids_dict = event_service.select_events(start_season)

# Insert Event Photos
event_photos_page.insert_event_photos(event_ids_dict)

# Event Stats
event_stats_page.insert_event_stats(event_ids_dict)

# Event Timetable
event_timetable_page.insert_timetable(event_ids_dict)

# Entries
entry_page.insert_entries(event_ids_dict, championship_list)

# Results
events_list = entry_service.select_events_without_results()
result_page.insert_results(events_list)

# Select Entries Data
driver_list = entry_service.select_drivers()
codriver_list = entry_service.select_codrivers()

# Drivers
profile_page.insert_drivers(driver_list, app.CATEGORY)

# Codrivers
coprofile_page.insert_codrivers(codriver_list, app.CATEGORY)

print('Execution Finish'.center(50, '-'))
