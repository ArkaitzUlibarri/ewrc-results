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

# Clear console
os.system("cls")

package_dir = os.path.abspath(os.path.dirname(__file__))
db = os.path.join(package_dir, 'database', app.database + '.db')

# Migrations
migrate(db)
seeder(db)

# Events
season.insert_events(app.base_url, db, app.database, app.start_season)

# Entries
event_ids_dict = select_events(db, app.start_season)
entries.insert_entries(app.base_url, db, event_ids_dict)

# Event Stats
eventstats.insert_event_stats(app.base_url, db, event_ids_dict)

# Drivers & Results
driver_list = select_drivers(db)
profile.insert_profiles(app.base_url, db, driver_list, app.category)

# Codrivers
codriver_list = select_codrivers(db)
coprofile.insert_codrivers(app.base_url, db, codriver_list, app.category)

# Event Photos
photo.insert_event_photos(app.base_url, db, event_ids_dict)

print('Finished')
