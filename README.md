# Workout Tracker

A Flask + SQLAlchemy + Marshmallow backend for a workout tracking app used by personal trainers.
It tracks workouts, reusable exercises, and the sets, reps or duration of each exercise inside a workout.

## Installation

1. Clone the repo and move into it:
   ```bash
   git clone <your-repo-ssh-or-https-link>
   cd workout-lab
   ```
2. Install dependencies and open the virtual environment:
   ```bash
   pipenv install
   pipenv shell
   ```
3. Create the database and load example data:
   ```bash
   cd server
   export FLASK_APP=app.py
   flask db upgrade head
   python seed.py
   ```

`python seed.py` can be re-run at any time to reset the data.

## Run

From the `server` folder:

```bash
flask run --port 5555
```

The API is then available at `http://127.0.0.1:5555`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show one workout with its exercises, including reps, sets and duration |
| POST | `/workouts` | Create a workout. Body: `date` (YYYY-MM-DD), `duration_minutes`, optional `notes` |
| DELETE | `/workouts/<id>` | Delete a workout and its associated WorkoutExercises |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show one exercise and the workouts it appears in |
| POST | `/exercises` | Create an exercise. Body: `name`, `category`, optional `equipment_needed` |
| DELETE | `/exercises/<id>` | Delete an exercise and its associated WorkoutExercises |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout. Body: `reps` and/or `duration_seconds`, optional `sets` |

Valid categories: strength, cardio, flexibility, balance, core.

Errors are returned as JSON: `400` for invalid data, `404` when a record isn't found, `409` when a database constraint is violated (for example a duplicate).

## Validations

- **Table constraints:** unique exercise names, non-blank name, valid category, positive duration, notes length limit, positive reps/sets/duration_seconds, and a unique (workout, exercise) pair.
- **Model validations:** `@validates` checks on names, categories, duration, notes, dates and reps/sets/duration_seconds.
- **Schema validations:** required fields, value ranges, allowed categories, no future dates, and a rule that reps or duration_seconds must be provided when adding an exercise to a workout.