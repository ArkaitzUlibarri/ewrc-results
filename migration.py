import logging

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

logging.basicConfig(
    filename='storage/logs/migrations.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format="%(asctime)s;%(levelname)s;%(message)s"
)
logging.info('Execution Start')

# DATABASE MIGRATION & SEEDING
logging.info('Migrations Start')

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

logging.info('Migrations End')

logging.info('Seeders Start')

points_seeder.run()

logging.info('Seeders End')
