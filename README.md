# Workout Tracker API

A Flask and SQLAlchemy backend for a workout tracking application used by personal trainers. The API manages workouts, reusable exercises, and the join records that attach exercises to a workout with reps, sets, and duration.

## Description

The app is built around three models:

- **Exercise** - a reusable exercise definition (name, category, whether equipment is needed).
- **Workout** - a single workout session (date, duration in minutes, notes).
- **WorkoutExercise** - the join table connecting a workout to an exercise, storing reps, sets, and duration in seconds for that specific pairing.

A workout has many exercises through workout_exercises, and an exercise has many workouts through workout_exercises. Data is validated at three levels: database table constraints, model-level validations, and Marshmallow schema validations.

## Installation

This project uses Pipenv.

```
pipenv install
pipenv shell
```

Then set up the database:

```
cd server
export FLASK_APP=app.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade head
python seed.py
```

## Running the app

From inside the `server/` directory:

```
python app.py
```

The API runs at `http://localhost:5555`.

## Endpoints

- `GET /workouts` - list all workouts.
- `GET /workouts/<id>` - show a single workout, including its workout_exercises with reps, sets, duration, and exercise info.
- `POST /workouts` - create a workout. Body: `date`, `duration_minutes`, `notes` (optional).
- `DELETE /workouts/<id>` - delete a workout and its associated workout_exercises.
- `GET /exercises` - list all exercises.
- `GET /exercises/<id>` - show a single exercise, including the workouts it belongs to.
- `POST /exercises` - create an exercise. Body: `name`, `category`, `equipment_needed`.
- `DELETE /exercises/<id>` - delete an exercise and its associated workout_exercises.
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` - attach an exercise to a workout. Body: any of `reps`, `sets`, `duration_seconds` (at least one required).

## Validations

Table constraints:
- Exercise name is unique.
- Workout duration_minutes must be greater than 0.
- WorkoutExercise reps, sets, and duration_seconds cannot be negative.

Model validations:
- Exercise name cannot be blank, category must be one of the allowed categories.
- Workout duration_minutes must be a positive integer, date is required.
- WorkoutExercise reps, sets, duration_seconds cannot be negative.

Schema validations:
- Exercise name and category are required and category must be one of the allowed categories.
- Workout duration_minutes must be a positive integer.
- WorkoutExercise requires at least one of reps, sets, or duration_seconds, and neither reps nor sets can be negative.

## Project structure

server/app.py Flask app and routes, server/models.py SQLAlchemy models, server/schemas.py Marshmallow schemas, server/seed.py seed data script.

## Tests

No automated test files are included in this submission.