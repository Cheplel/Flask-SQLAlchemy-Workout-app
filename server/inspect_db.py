from sqlalchemy import text
from server.app import app
from server.models import db

print('app db uri:', app.config['SQLALCHEMY_DATABASE_URI'])
with app.app_context():
    engine = db.engine
    print('engine url:', engine.url)
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ")).fetchall()
        print('tables', rows)
        try:
            count = conn.execute(text('SELECT count(*) FROM exercises')).scalar()
            print('exercise_count', count)
        except Exception as exc:
            print('exercise_error', repr(exc))
