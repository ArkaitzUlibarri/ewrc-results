import os
from config import app
from database.migration import migrate
from database.seeders.championshipPoints import seeder
from database.helper import select_events
from database.helper import select_drivers
from database.helper import select_codrivers
from pages import season
from pages import entries
from pages import eventstats
from pages import photo
from pages import profile
from pages import coprofile
from pages import timetable

# Clear console
os.system("cls")

package_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(package_dir, 'database', app.database + '.db')

# Migrations
migrate(db_path)
seeder(db_path)

# Events
season_list = season.get_seasons(app.base_url)
nationality_list = season.get_nationalities(app.base_url, app.start_season)
category_list = season.get_championships(app.base_url, app.start_season, '95')

season.insert_events(app.base_url, db_path, app.database, app.start_season)

# Entries
event_ids_dict = select_events(db_path, app.start_season)
entries.insert_entries(app.base_url, db_path, event_ids_dict)

# Event Stats
eventstats.insert_event_stats(app.base_url, db_path, event_ids_dict)

# Timetable
timetable.get_timetable(app.base_url, db_path, event_ids_dict)

# Drivers & Results
driver_list = select_drivers(db_path)
profile.insert_profiles(app.base_url, db_path, driver_list, app.category)

# Codrivers
codriver_list = select_codrivers(db_path)
coprofile.insert_codrivers(app.base_url, db_path, codriver_list, app.category)

# Event Photos
photo.insert_event_photos(app.base_url, db_path, event_ids_dict)

print('Finished')
