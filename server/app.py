from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError

# Support running as package (`python -m server.app`) and as script (`python server/app.py`).
try:
    from server.models import db, Exercise, Workout, WorkoutExercises
    from server.schemas import ExerciseSchema, WorkoutSchema, WorkoutExercisesSchema
except Exception:
    # fallback to local imports when running the script directly
    from models import db, Exercise, Workout, WorkoutExercises
    from schemas import ExerciseSchema, WorkoutSchema, WorkoutExercisesSchema

app = Flask(__name__)
# Use the absolute instance DB file path so the app always opens the seeded file.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Dell/Desktop/Flask SQLAlchemy Workout app/instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
exercise_list_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workout_list_schema = WorkoutSchema(many=True)
workout_exercises_schema = WorkoutExercisesSchema()
workout_exercises_list_schema = WorkoutExercisesSchema(many=True)


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({"errors": error.messages}), 400


# Define Routes here
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Workout App!"}), 200

# List all workouts
@app.route('/workouts', methods=['GET'])
def list_workouts():
    workouts = Workout.query.all()

    print("Workout count:", len(workouts))
    for w in workouts:
        print(w.id, w.notes)

    return jsonify({"workouts": workout_list_schema.dump(workouts)}), 200

# Show single workout with specific id
@app.route('/workouts/<int:workout_id>', methods=['GET'])
def show_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify({"workout": workout_schema.dump(workout)}), 200

# Create a workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json() or {}
    workout = workout_schema.load(data)
    db.session.add(workout)
    db.session.commit()
    return jsonify({"workout": workout_schema.dump(workout)}), 201


    

# List all exercises
@app.route('/exercises', methods=['GET'])
def list_exercises():
    exercises = Exercise.query.all()
    return jsonify({"exercises": exercise_list_schema.dump(exercises)}), 200

# Show single exercise with specific id
@app.route('/exercises/<int:exercise_id>', methods=['GET'])
def show_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify({"exercise": exercise_schema.dump(exercise)}), 200

# Create an exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = request.get_json() or {}
        exercise = exercise_schema.load(data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify({"exercise": exercise_schema.dump(exercise)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Add an exercise to a workout, including reps/sets/duration
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
        return jsonify({"error": "Workout or exercise not found"}), 404

    data = request.get_json() or {}

    workout_exercise = WorkoutExercises(
        workout_id=workout_id,
        exercise_id=exercise_id,
        sets=data.get("sets"),
        reps=data.get("reps"),
        duration_seconds=data.get("duration_seconds")
    )

    db.session.add(workout_exercise)
    db.session.commit()

    return jsonify({
        "message": "Exercise added to workout"
    }), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)