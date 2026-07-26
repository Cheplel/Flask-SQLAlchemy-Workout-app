import os
import sqlite3

path = r'C:/Users/Dell/Desktop/Flask SQLAlchemy Workout app/instance/app.db'
print('exists', os.path.exists(path))
print('abspath', os.path.abspath(path))
conn = sqlite3.connect(path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('tables', cur.fetchall())
try:
    cur.execute('SELECT count(*) FROM exercises')
    print('exercise_count', cur.fetchone()[0])
except Exception as e:
    print('exercise_error', repr(e))
conn.close()
