from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

db = SQLAlchemy()

ALLOWED_CATEGORIES = {"strength", "cardio", "mobility", "balance", "flexibility"}


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (
        db.UniqueConstraint("name", name="uq_exercise_name"),
    )

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan"
    )
    workouts = association_proxy("workout_exercises", "workout")

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("name must not be empty")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if not value or value.lower() not in ALLOWED_CATEGORIES:
            raise ValueError(f"category must be one of {sorted(ALLOWED_CATEGORIES)}")
        return value.lower()

    def __repr__(self):
        return f"<Exercise {self.id} {self.name}>"


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint("duration_minutes > 0", name="ck_workout_duration_positive"),
    )

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan"
    )
    exercises = association_proxy("workout_exercises", "exercise")

    @validates("duration_minutes")
    def validate_duration_minutes(self, key, value):
        if value is None or value <= 0:
            raise ValueError("duration_minutes must be a positive integer")
        return value

    @validates("date")
    def validate_date(self, key, value):
        if not value:
            raise ValueError("date is required")
        return value

    def __repr__(self):
        return f"<Workout {self.id} {self.date}>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        db.CheckConstraint("reps IS NULL OR reps >= 0", name="ck_we_reps_nonneg"),
        db.CheckConstraint("sets IS NULL OR sets >= 0", name="ck_we_sets_nonneg"),
        db.CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds >= 0",
            name="ck_we_duration_nonneg",
        ),
    )

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value < 0:
            raise ValueError("reps cannot be negative")
        return value

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value < 0:
            raise ValueError("sets cannot be negative")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and value < 0:
            raise ValueError("duration_seconds cannot be negative")
        return value

    def __repr__(self):
        return f"<WorkoutExercise {self.id} workout={self.workout_id} exercise={self.exercise_id}>"