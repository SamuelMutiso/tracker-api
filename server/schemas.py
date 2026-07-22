from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError

ALLOWED_CATEGORIES = {"strength", "cardio", "mobility", "balance", "flexibility"}


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1))
    category = fields.String(required=True)
    equipment_needed = fields.Boolean(required=True)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("name must not be blank")

    @validates("category")
    def validate_category(self, value, **kwargs):
        if value.lower() not in ALLOWED_CATEGORIES:
            raise ValidationError(f"category must be one of {sorted(ALLOWED_CATEGORIES)}")


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1))
    notes = fields.String(allow_none=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)
    reps = fields.Integer(allow_none=True)
    sets = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates("reps")
    def validate_reps(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError("reps cannot be negative")

    @validates("sets")
    def validate_sets(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError("sets cannot be negative")

    @validates_schema
    def validate_has_a_metric(self, data, **kwargs):
        if data.get("reps") is None and data.get("sets") is None and data.get("duration_seconds") is None:
            raise ValidationError("at least one of reps, sets or duration_seconds is required")


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


class WorkoutExerciseForExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    reps = fields.Integer(dump_only=True)
    sets = fields.Integer(dump_only=True)
    duration_seconds = fields.Integer(dump_only=True)
    workout = fields.Nested(WorkoutSchema, dump_only=True)


class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.Nested(WorkoutExerciseForExerciseSchema, many=True, dump_only=True)