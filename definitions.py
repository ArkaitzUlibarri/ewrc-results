import os

from config import app

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, 'database', app.DATABASE + '.db')
EXPORT_FOLDER = os.path.join(ROOT_DIR, 'storage', 'exports')
