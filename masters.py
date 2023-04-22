import datetime

from pages import season as season_page
from services import nationality_service

# NATIONALITIES & CHAMPIONSHIPS

# Season Options
season_list = season_page.get_seasons()
start_season = season_list[-1]

# Insert actual season nationalities
actual_year = datetime.date.today().year
season_page.insert_nationalities(actual_year)

# Select FIA nationality
nationality = nationality_service.select_nationality('FIA')

# Insert FIA championships
for item in season_list:
    season_page.insert_championships(item, nationality)
