import pandas as pd
import sqlite3

df = pd.read_csv('DATA/cyber_incidents.csv')

databaseLoc = 'DATA/cyberincidents1.db'
conn = sqlite3.connect(DB_PATH)
df.to_sql('cyberincidents', conn, if_exists='append', index=False)