from sqlite3 import connect
from pathlib import Path

path = Path('app.db')
if not path.exists():
    raise SystemExit('app.db not found')

conn = connect(path)
cur = conn.cursor()

for tbl in ['exercises', 'workouts', 'workout_exercises']:
    try:
        cur.execute(f'SELECT count(*) FROM {tbl}')
        print(tbl, cur.fetchone()[0])
    except Exception as e:
        print(tbl, 'error', e)

print('\nExercises:')
for row in cur.execute('SELECT name, category, equipment FROM exercises'):
    print(row)

print('\nWorkouts:')
for row in cur.execute('SELECT date, duration, notes FROM workouts'):
    print(row)

print('\nWorkoutExercises:')
for row in cur.execute('SELECT workout_id, exercise_id, reps, sets, duration_seconds FROM workout_exercises'):
    print(row)

conn.close()
