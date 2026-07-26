from datetime import date

from marshmallow import Schema, ValidationError, fields, post_load, validates, validates_schema

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

    @validates('reps')
    def validate_reps(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError('reps must be a non-negative integer')
        return value

    @validates('sets')
    def validate_sets(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError('sets must be a non-negative integer')
        return value

    @validates('duration_seconds')
    def validate_duration_seconds(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError('duration_seconds must be a non-negative integer')
        return value

    @validates_schema
    def validate_reps_or_duration(self, data, **kwargs):
        reps = data.get('reps')
        duration = data.get('duration_seconds')
        # require at least one of reps/sets or duration_seconds when creating an association
        if (reps is None or reps == 0) and (duration is None or duration == 0):
            # allow zero only if the other field is present; otherwise require a positive value
            raise ValidationError("Either 'reps' (positive) or 'duration_seconds' (positive) must be provided.")


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
    def validate_category(self, value, **kwargs):
        if value not in ALLOWED_CATEGORIES:
            raise ValidationError(
                f"Category must be one of {ALLOWED_CATEGORIES}."
            )
        return value

    @validates('name')
    def validate_name(self, value, **kwargs):
        if not value or not value.strip():
            raise ValidationError('name must not be blank')
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
    def validate_duration(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("Duration must be a positive integer.")
        return value

    @validates("date")
    def validate_date(self, value, **kwargs):
        if value > date.today():
            raise ValidationError("Date cannot be in the future.")
        return value

    @validates_schema
    def validate_workout_fields(self, data, **kwargs):
        # ensure duration is present and positive (field validator covers value, this ensures presence)
        if 'duration' not in data:
            raise ValidationError({'duration': ['Missing data for required field.']})

    @post_load
    def make_workout(self, data, **kwargs):
        return Workout(**data)
