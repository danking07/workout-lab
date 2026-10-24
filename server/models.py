from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

db = SQLAlchemy()

CATEGORIES = ["strength", "cardio", "flexibility", "balance", "core"]


class Exercise(db.Model):
    __tablename__ = "exercises"

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="ck_exercise_name_not_blank"),
        CheckConstraint(
            "category IN ('strength','cardio','flexibility','balance','core')",
            name="ck_exercise_category_valid",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan"
    )
    workouts = association_proxy("workout_exercises", "workout")

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Exercise name cannot be blank.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if value not in CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(CATEGORIES)}.")
        return value


class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="ck_workout_duration_positive"),
        CheckConstraint(
            "notes IS NULL OR length(notes) <= 500", name="ck_workout_notes_length"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan"
    )
    exercises = association_proxy("workout_exercises", "exercise")

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("duration_minutes must be a positive integer.")
        return value

    @validates("notes")
    def validate_notes(self, key, value):
        if value is not None and len(value) > 500:
            raise ValueError("Notes cannot exceed 500 characters.")
        return value

    @validates("date")
    def validate_date(self, key, value):
        if value > date.today():
            raise ValueError("Workout date cannot be in the future.")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    __table_args__ = (
        UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise"),
        CheckConstraint("reps IS NULL OR reps > 0", name="ck_we_reps_positive"),
        CheckConstraint("sets IS NULL OR sets > 0", name="ck_we_sets_positive"),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="ck_we_duration_positive",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps", "sets", "duration_seconds")
    def validate_positive(self, key, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError(f"{key} must be a positive integer.")
        return value