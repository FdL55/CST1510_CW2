import sqlite3

from dbHelper import DB_PATH

conn = sqlite3.connect('DATA/cyberincidents.db')
cursor = conn.cursor()
createcyberinc = """ CREATE TABLE IF NOT EXISTS cyber_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    i_date TEXT,
    i_type TEXT,
    severity TEXT,
    status TEXT,
    description TEXT,
    reported_by TEXT DEFAULT system,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP )"""
cursor.execute(createcyberinc)
conn.commit()
