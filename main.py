import os
from config import app
from database.migration import migrate
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
dbPath = os.path.join(packageDir,'database', app.database + '.db')

# Migrations
migrate(dbPath)

# Events
season.insertEvents(app.base_url, dbPath, app.database, app.startSeason)

# Entries
event_ids_dict = selectEvents(dbPath, app.startSeason)
entries.insertEntries(app.base_url,dbPath,event_ids_dict)

# Event Stats
eventstats.insertEventStats(app.base_url,dbPath,event_ids_dict)

# Drivers & Results
driverlist = selectDrivers(dbPath)
profile.insertDriversAndResults(app.base_url, dbPath, driverlist, app.category)

# Codrivers
codriverlist = selectCodrivers(dbPath)
coprofile.insertCodrivers(app.base_url, dbPath, codriverlist, app.category)

# Event Photos
photo.insertEventPhotos(app.base_url,dbPath,event_ids_dict)
