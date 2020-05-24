import os
from config import app
from database.migration import migrate
from database.seeders.championshipPoints import seeder
from database.helper import selectEvents
from database.helper import selectDrivers
from database.helper import selectCodrivers
from pages import season
from pages import entries
from pages import eventstats
from pages import photo
from pages import profile
from pages import coprofile

 # Clear console
os.system("cls") 

packageDir  = os.path.abspath(os.path.dirname(__file__))
db = os.path.join(packageDir,'database', app.database + '.db')

# Migrations
migrate(db)
seeder(db)

# Events
season.insertEvents(app.base_url, db, app.database, app.startSeason)

# Entries
event_ids_dict = selectEvents(db, app.startSeason)
entries.insertEntries(app.base_url,db,event_ids_dict)

# Event Stats
eventstats.insertEventStats(app.base_url,db,event_ids_dict)

# Drivers & Results
driverlist = selectDrivers(db)
profile.insertDriversAndResults(app.base_url, db, driverlist, app.category)

# Codrivers
codriverlist = selectCodrivers(db)
coprofile.insertCodrivers(app.base_url, db, codriverlist, app.category)

# Event Photos
photo.insertEventPhotos(app.base_url,db,event_ids_dict)
