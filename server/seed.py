#!/usr/bin/env python3
from datetime import date, timedelta

from app import app
from models import Exercise, Workout, WorkoutExercise, db

with app.app_context():
    print("Clearing old data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    squat = Exercise(name="Squat", category="strength", equipment_needed=True)
    pushup = Exercise(name="Push-up", category="strength", equipment_needed=False)
    run = Exercise(name="Treadmill Run", category="cardio", equipment_needed=True)
    plank = Exercise(name="Plank", category="core", equipment_needed=False)
    stretch = Exercise(name="Hamstring Stretch", category="flexibility", equipment_needed=False)
    db.session.add_all([squat, pushup, run, plank, stretch])

    print("Seeding workouts...")
    today = date.today()
    w1 = Workout(date=today - timedelta(days=2), duration_minutes=45, notes="Leg day")
    w2 = Workout(date=today - timedelta(days=1), duration_minutes=30, notes="Cardio and core")
    w3 = Workout(date=today, duration_minutes=60, notes="Full body")
    db.session.add_all([w1, w2, w3])
    db.session.flush()

    print("Linking exercises to workouts...")
    db.session.add_all([
        WorkoutExercise(workout_id=w1.id, exercise_id=squat.id, reps=10, sets=4),
        WorkoutExercise(workout_id=w1.id, exercise_id=stretch.id, duration_seconds=60, sets=2),
        WorkoutExercise(workout_id=w2.id, exercise_id=run.id, duration_seconds=1200),
        WorkoutExercise(workout_id=w2.id, exercise_id=plank.id, duration_seconds=60, sets=3),
        WorkoutExercise(workout_id=w3.id, exercise_id=squat.id, reps=8, sets=3),
        WorkoutExercise(workout_id=w3.id, exercise_id=pushup.id, reps=15, sets=3),
        WorkoutExercise(workout_id=w3.id, exercise_id=plank.id, duration_seconds=45, sets=3),
    ])
    db.session.commit()
    print("Done!")