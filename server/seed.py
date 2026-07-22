#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("clearing tables")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("seeding exercises")
    push_up = Exercise(name="Push Up", category="strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="strength", equipment_needed=False)
    plank = Exercise(name="Plank", category="mobility", equipment_needed=False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    bench_press = Exercise(name="Bench Press", category="strength", equipment_needed=True)

    db.session.add_all([push_up, squat, plank, running, bench_press])
    db.session.commit()

    print("seeding workouts")
    workout_one = Workout(date=date(2026, 7, 1), duration_minutes=45, notes="upper body day")
    workout_two = Workout(date=date(2026, 7, 3), duration_minutes=30, notes="core and cardio")

    db.session.add_all([workout_one, workout_two])
    db.session.commit()

    print("seeding workout exercises")
    workout_exercise_one = WorkoutExercise(
        workout_id=workout_one.id, exercise_id=push_up.id, reps=15, sets=3
    )
    workout_exercise_two = WorkoutExercise(
        workout_id=workout_one.id, exercise_id=bench_press.id, reps=10, sets=4
    )
    workout_exercise_three = WorkoutExercise(
        workout_id=workout_two.id, exercise_id=plank.id, duration_seconds=60
    )
    workout_exercise_four = WorkoutExercise(
        workout_id=workout_two.id, exercise_id=running.id, duration_seconds=1200
    )

    db.session.add_all(
        [
            workout_exercise_one,
            workout_exercise_two,
            workout_exercise_three,
            workout_exercise_four,
        ]
    )
    db.session.commit()

    print("done seeding")