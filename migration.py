import os

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

os.system("cls")

print('Execution Start'.center(50, '-'))

# DATABASE MIGRATION & SEEDING
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
