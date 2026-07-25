from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment = db.Column(db.Boolean)

    workouts = db.relationship('Workout', back_populates='exercise')

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration = db.Column(db.Integer)  # duration in minutes
    notes = db.Column(db.text)

    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    exercise = db.relationship('Exercise', back_populates='workouts')

