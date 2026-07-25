#!/usr/bin/env python3

from datetime import date

from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercises

with app.app_context():
    # Remove existing seed data if present
    WorkoutExercises.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # Create example exercises
    pushups = Exercise(name='Push-ups', category='Chest', equipment=False)
    squats = Exercise(name='Squats', category='Legs', equipment=False)
    deadlift = Exercise(name='Deadlift', category='Back', equipment=False)
    running = Exercise(name='Running', category='Cardio', equipment=False)

    db.session.add_all([pushups, squats, deadlift, running])
    db.session.commit()

    # Create a workout and assign exercises through the association table
    workout = Workout(date=date.today(), duration=40, notes='Full-body workout')
    db.session.add(workout)
    db.session.commit()

    workout_exercise_1 = WorkoutExercises(
        workout=workout,
        exercise=pushups,
        reps=15,
        sets=3,
        duration_seconds=20,
    )
    workout_exercise_2 = WorkoutExercises(
        workout=workout,
        exercise=squats,
        reps=20,
        sets=3,
        duration_seconds=20,
    )
    workout_exercise_3 = WorkoutExercises(
        workout=workout,
        exercise=deadlift,
        reps=10,
        sets=3,
        duration_seconds=60,
    )
    workout_exercise_4 = WorkoutExercises(
        workout=workout,
        exercise=running,
        reps=None,
        sets=None,
        duration_seconds=1200,
    )

    db.session.add_all([workout_exercise_1, workout_exercise_2, workout_exercise_3, workout_exercise_4])
    db.session.commit()

    print('Seed data created successfully.')
