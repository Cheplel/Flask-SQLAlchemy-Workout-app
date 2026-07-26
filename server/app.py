from flask import Flask, make_response, request
from flask_migrate import Migrate

from server.models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here
@app.route('/')
def index():
    return make_response({"message": "Welcome to the Workout App!"}, 200)

#List all workouts
@app.route('/workouts', methods=['GET'])
def list_workouts():
    workouts = Workout.query.all()
    return make_response({"workouts": [workout.to_dict() for workout in workouts]}, 200)

#Show single workout with specific id
@app.route('/workouts/<int:workout_id>', methods=['GET'])
def show_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    return make_response({"workout": workout.to_dict()}, 200)

#Create a workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    workout = Workout(
        date=data['date'],
        duration=data['duration'],
        notes=data['notes']
    )
    db.session.add(workout)
    db.session.commit()
    return make_response({"workout": workout.to_dict()}, 201)

#List all exercises
@app.route('/exercises', methods=['GET'])
def list_exercises():
    exercises = Exercise.query.all()
    return make_response({"exercises": [exercise.to_dict() for exercise in exercises]}, 200)

#Show single exercise with specific id
@app.route('/exercises/<int:exercise_id>', methods=['GET'])
def show_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    return make_response({"exercise": exercise.to_dict()}, 200)

#Create an exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    exercise = Exercise(
        name=data['name'],
        description=data['description']
    )
    db.session.add(exercise)
    db.session.commit()
    return make_response({"exercise": exercise.to_dict()}, 201)

#Add an exercise to a workout, including reps/sets/duration
@app.route('/workouts/<int:workout_id>/exercises', methods=['POST'])
def add_exercise_to_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    data = request.get_json()
    exercise_id = data['exercise_id']
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    workout_exercise = WorkoutExercises(
        workout=workout,
        exercise=exercise,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )
    db.session.add(workout_exercise)
    db.session.commit()
    return make_response({"workout_exercise": workout_exercise.to_dict()}, 201)




if __name__ == '__main__':
    app.run(port=5555, debug=True)