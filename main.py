import os
from config import app
from database import migration
from database import seeder
from database import helper as db_helper
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

package_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(package_dir, 'database', app.database + '.db')

# Migrations
migration.migrate(db_path)
seeder.championship_points(db_path)

# Season Options
season_list = season_page.get_seasons(app.base_url)
start_season = season_list[-1]

for item in season_list:
    season_page.insert_nationalities(app.base_url, db_path, item)

nationality_list = db_helper.select_nationalities(db_path)

for item in season_list:
    for index, row in enumerate(nationality_list, start=1):
        season_page.insert_championships(app.base_url, db_path, item, row['id'])

# Events
season_page.insert_events(app.base_url, db_path, start_season, "1-wrc")

# Select Events Data
championship_list = db_helper.select_championships(db_path)
event_ids_dict = db_helper.select_events(db_path, start_season)

# Event Photos
event_photos_page.insert_event_photos(app.base_url, db_path, event_ids_dict)

# Event Stats
event_stats_page.insert_event_stats(app.base_url, db_path, event_ids_dict)

# Event Timetable
event_timetable_page.get_timetable(app.base_url, db_path, event_ids_dict)

# Entries
entry_page.insert_entries(app.base_url, db_path, event_ids_dict, championship_list)

# Results
result_page.insert_results(app.base_url, db_path, event_ids_dict)

# Select Entries Data
driver_list = db_helper.select_drivers(db_path)
codriver_list = db_helper.select_codrivers(db_path)

# Drivers
profile_page.insert_drivers(app.base_url, db_path, driver_list, app.category)

# Codrivers
coprofile_page.insert_codrivers(app.base_url, db_path, codriver_list, app.category)

print('Finished')
