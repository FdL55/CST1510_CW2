import sqlite3
from pathlib import Path

DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "cyberincidents.db"

def connect_database(db_path=DB_PATH):
    return sqlite3.connect(str(db_path))