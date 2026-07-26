import json
import sys
import pathlib
import pytest

# Ensure project root is on sys.path so `server` package is importable when pytest runs
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from server.app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_create_workout_negative_duration(client):
    payload = {"date": "2026-07-26", "duration": -10}
    resp = client.post('/workouts', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 400
    body = resp.get_json()
    assert 'duration' in json.dumps(body) or 'Duration' in json.dumps(body)


def test_create_exercise_invalid_category(client):
    payload = {"name": "Test", "category": "InvalidCategory", "equipment": False}
    resp = client.post('/exercises', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 400
    body = resp.get_json()
    assert 'Category must be one of' in json.dumps(body)


def test_association_requires_reps_or_duration(client):
    # create exercise
    exercise_payload = {"name": "Tmp", "category": "Chest", "equipment": False}
    resp = client.post('/exercises', data=json.dumps(exercise_payload), content_type='application/json')
    assert resp.status_code == 201
    ex = resp.get_json()['exercise']

    # create workout
    workout_payload = {"date": "2026-07-26", "duration": 30}
    resp = client.post('/workouts', data=json.dumps(workout_payload), content_type='application/json')
    assert resp.status_code == 201
    wk = resp.get_json()['workout']

    # attempt to add association with neither reps nor duration_seconds
    assoc_payload = {"exercise_id": ex['id']}
    resp = client.post(f"/workouts/{wk['id']}/exercises", data=json.dumps(assoc_payload), content_type='application/json')
    assert resp.status_code == 400
    body = resp.get_json()
    assert 'Either' in json.dumps(body) or 'reps' in json.dumps(body)


def test_valid_create_flow_returns_201(client):
    exercise_payload = {"name": "ValidEx", "category": "Chest", "equipment": False}
    resp = client.post('/exercises', data=json.dumps(exercise_payload), content_type='application/json')
    assert resp.status_code == 201

    workout_payload = {"date": "2026-07-26", "duration": 45}
    resp = client.post('/workouts', data=json.dumps(workout_payload), content_type='application/json')
    assert resp.status_code == 201
    wk = resp.get_json()['workout']

    ex = client.get('/exercises').get_json()['exercises'][0]
    assoc_payload = {"exercise_id": ex['id'], "reps": 10, "sets": 3}
    resp = client.post(f"/workouts/{wk['id']}/exercises", data=json.dumps(assoc_payload), content_type='application/json')
    assert resp.status_code == 201
