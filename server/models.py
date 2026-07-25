from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False, unique=True)
    category = db.Column(db.String(90), nullable=False)
    equipment = db.Column(db.Boolean, default=False)

    @validates('category')
    def validate_category(self, key, value):
        allowed_categories = ['Cardio', 'Strength', 'Flexibility', 'Balance']
        if value not in allowed_categories:
            raise ValueError(f"Category must be one of {allowed_categories}.")
        return value

    workout_exercises = db.relationship(
        'WorkoutExercises',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        viewonly=True
    )

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # duration in minutes
    notes = db.Column(db.Text)

    @validates('duration')
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be a positive integer.")
        return value
    @validates('date')
    def validate_date(self, key, value):
        from datetime import date as dt_date
        if value > dt_date.today():
            raise ValueError("Date cannot be in the future.")
        return value

    workout_exercises = db.relationship(
        'WorkoutExercises',
        back_populates='workout',
        cascade='all, delete-orphan'
    )
    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts',
        viewonly=True
    )

class WorkoutExercises(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} must be a non-negative integer.")
        return value
    

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')