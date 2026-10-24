from datetime import date

from marshmallow import Schema, ValidationError, fields, validate, validates, validates_schema

from models import CATEGORIES


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(CATEGORIES))
    equipment_needed = fields.Bool(load_default=False)

    @validates("name")
    def validate_name_not_blank(self, value):
        if not value.strip():
            raise ValidationError("Name cannot be blank.")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(load_default=None, allow_none=True, validate=validate.Length(max=500))

    @validates("date")
    def validate_date_not_future(self, value):
        if value > date.today():
            raise ValidationError("Date cannot be in the future.")


class WorkoutExerciseSchema(Schema):
    """Used to validate the body of 'add exercise to workout'."""

    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(load_default=None, allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(load_default=None, allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(
        load_default=None, allow_none=True, validate=validate.Range(min=1)
    )

    @validates_schema
    def require_some_measure(self, data, **kwargs):
        if data.get("reps") is None and data.get("duration_seconds") is None:
            raise ValidationError("Provide reps or duration_seconds.", "reps")


class WorkoutExerciseWithExerciseSchema(WorkoutExerciseSchema):
    """Workout detail view: each entry includes its exercise."""

    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutExerciseWithWorkoutSchema(WorkoutExerciseSchema):
    """Exercise detail view: each entry includes its workout."""

    workout = fields.Nested(WorkoutSchema, dump_only=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(WorkoutExerciseWithExerciseSchema, many=True, dump_only=True)


class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.Nested(WorkoutExerciseWithWorkoutSchema, many=True, dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()
workout_exercise_schema = WorkoutExerciseSchema()