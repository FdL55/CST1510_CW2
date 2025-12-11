# dbHelper.py
import sqlite3
from pathlib import Path
import pandas as pd

# =============================
# DATABASE PATH
# =============================
DB_PATH = Path("cyberincidents.db")   # Single DB for everything


# =============================
# SQL SCHEMA (ALL TABLES)
# =============================
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cyber_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    i_date TEXT,
    i_type TEXT,
    severity TEXT,
    status TEXT,
    description TEXT,
    reported_by TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


# =============================
# CONNECT TO DATABASE
# =============================
def connect_database(db_path: str = None):
    """Returns sqlite3 connection with Row factory."""
    path = str(DB_PATH if db_path is None else db_path)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# =============================
# INITIALISE DATABASE TABLES
# =============================
def init_db(conn=None):
    """
    Creates all tables needed for the system.
    This function runs automatically on app start.
    """
    close_after = False

    if conn is None:
        conn = connect_database()
        close_after = True

    cur = conn.cursor()
    cur.executescript(SCHEMA_SQL)
    conn.commit()

    if close_after:
        conn.close()


# =============================
# LOAD CSV → DATABASE
# =============================
def load_csv_to_db(csv_path, table_name="cyber_incidents", conn=None, if_exists="append"):
    """Loads CSV data into a table (used for initial data import)."""
    df = pd.read_csv(csv_path)

    close_after = False
    if conn is None:
        conn = connect_database()
        close_after = True

    df.to_sql(table_name, conn, if_exists=if_exists, index=False)

    if close_after:
        conn.close()


# =============================
# READ INCIDENTS (OPTIONAL)
# =============================
def read_incidents(conn=None, filters=None):
    """Return incidents as a pandas DataFrame with optional filters."""
    close_after = False

    if conn is None:
        conn = connect_database()
        close_after = True

    sql = "SELECT * FROM cyber_incidents"
    params = []

    if filters:
        where = [f"{k} = ?" for k in filters]
        sql += " WHERE " + " AND ".join(where)
        params = list(filters.values())

    df = pd.read_sql_query(sql, conn, params=params)

    if close_after:
        conn.close()

    return df
