import sqlite3
databaseLoc = 'DATA/cyberincidents.db'

conn = sqlite3.connect(databaseLoc)
cursor = conn.cursor()


with open('DATA/cyber_incidents.csv', 'r') as cyber:
    i = 0
    for line in cyber.readlines():
        if i == 0:
            i +=1
            continue
        line = line.strip()
        vals = line.split(',')
        #vals[0],     #vals[1],  #vals[2], #vals[3], #vals[4], #vals[5]
        #incident_id, timestamp, severity, category, status, description
        insertScript = """insert into cyber_incidents(
            id, i_date, severity, i_type, status, description)
        values(?,?,?,?,?,?) """
        cursor.execute(insertScript, (vals[0], vals[1], vals[2], vals[3], vals[4], vals[5]))
        conn.commit()