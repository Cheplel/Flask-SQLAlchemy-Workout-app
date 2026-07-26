from datetime import date

from marshmallow import Schema, ValidationError, fields, post_load, validates

from server.models import Exercise, Workout, WorkoutExercises

ALLOWED_CATEGORIES = ["Chest", "Legs", "Back", "Cardio", "Strength"]


class WorkoutExercisesSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)
    workout = fields.Nested(
        "WorkoutSchema",
        only=("id", "date", "duration", "notes"),
        dump_only=True,
    )
    exercise = fields.Nested(
        "ExerciseSchema",
        only=("id", "name", "category", "equipment"),
        dump_only=True,
    )

    @post_load
    def make_workout_exercises(self, data, **kwargs):
        return WorkoutExercises(**data)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment = fields.Bool(required=True)
    workouts = fields.List(
        fields.Nested("WorkoutSchema", only=("id", "date", "duration")),
        dump_only=True,
    )
    workout_exercises = fields.List(
        fields.Nested(WorkoutExercisesSchema(exclude=("exercise",))),
        dump_only=True,
    )

    @validates("category")
    def validate_category(self, value):
        if value not in ALLOWED_CATEGORIES:
            raise ValidationError(
                f"Category must be one of {ALLOWED_CATEGORIES}."
            )
        return value

    @post_load
    def make_exercise(self, data, **kwargs):
        return Exercise(**data)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration = fields.Int(required=True)
    notes = fields.Str(allow_none=True)
    exercises = fields.List(
        fields.Nested(ExerciseSchema(only=("id", "name", "category", "equipment"))),
        dump_only=True,
    )
    workout_exercises = fields.List(
        fields.Nested(WorkoutExercisesSchema(exclude=("workout",))),
        dump_only=True,
    )

    @validates("duration")
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("Duration must be a positive integer.")
        return value

    @validates("date")
    def validate_date(self, value):
        if value > date.today():
            raise ValidationError("Date cannot be in the future.")
        return value

    @post_load
    def make_workout(self, data, **kwargs):
        return Workout(**data)
