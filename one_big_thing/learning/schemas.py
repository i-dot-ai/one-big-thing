from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates_schema,
)

from one_big_thing.learning.utils import is_civil_service_email

from . import choices, constants
from .models import Department

HOURS_ERROR = "Please enter the hours this course took to complete, for example, 2"
MINUTES_ERROR = "Please enter the minutes this course took to complete, between 0 and 59"


def validate_email(email):
    if not is_civil_service_email(email):
        raise ValidationError("This should be a valid Civil Service email")
    return True


class SingleLineStr(fields.Str):
    def _deserialize(self, value, attr, data, **kwargs):
        if value:
            single_line_value = " ".join(value.splitlines())
            if not value == single_line_value:
                raise ValidationError("Cannot contain linebreaks")
        return super()._deserialize(value, attr, data, **kwargs)


class LearningTitleSingleLineStr(SingleLineStr):
    def _deserialize(self, value, attr, data, **kwargs):
        if not value:
            raise ValidationError("Please provide a title for this course")
        elif len(value) > 200:
            raise ValidationError("The title must be less than 200 characters")
        return super()._deserialize(value, attr, data, **kwargs)


def validate_choice_and_length_or_none(values):
    def validator(value):
        if value != "" and not validate.OneOf(values):
            raise ValidationError(f"Value needs to be in {values} or None")

    return validator


def make_choice_field(max_len, values, allow_none=False, **kwargs):
    if allow_none:
        field = SingleLineStr(
            validate=validate.And(validate.Length(max=max_len), validate_choice_and_length_or_none(values)),
            allow_none=True,
            **kwargs,
        )
    else:
        field = SingleLineStr(validate=validate.And(validate.Length(max=max_len), validate.OneOf(values)), **kwargs)
    return field


class UserSchema(Schema):
    email = fields.Str(validate=validate_email)


class TimeStampedModelSchema(Schema):
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)


class UUIDPrimaryKeyBaseModelSchema(Schema):
    id = fields.UUID()


def get_error_message_for_integer_validation(
    value, max=None, error_msg="There is an error with this value", error_msg_max=""
):
    """
    Checks if value is a positive integer, optionally checks if below max.

    Args:
        value: Any value to be validated
        max: Optional value to check value is below max
        error_msg (str): General error message to display
        error_msg_max (str): Optional error message if number exceeds max, otherwise error_msg is displayed
    """
    if not value:
        return None
    try:
        value = int(value)
        if value < 0:
            return error_msg
        elif max and (value > max):
            if error_msg_max:
                return error_msg_max
            return error_msg
    except ValueError:
        return error_msg


def validate_time_to_complete(value):
    error_message = get_error_message_for_integer_validation(
        value, error_msg="Please enter the time this course took to complete in minutes, e.g. 15"
    )
    if error_message:
        raise ValidationError(error_message)


class CourseSchema(TimeStampedModelSchema, UUIDPrimaryKeyBaseModelSchema):
    title = SingleLineStr(required=True, validate=validate.Length(max=200))
    link = SingleLineStr(validate=validate.Length(max=256), allow_none=True)
    learning_type = make_choice_field(max_len=256, values=choices.CourseType.values, allow_none=True)
    time_to_complete = fields.Str(required=False, validate=validate_time_to_complete)


class LearningSchema(TimeStampedModelSchema, UUIDPrimaryKeyBaseModelSchema):
    title = SingleLineStr(required=True, validate=validate.Length(max=200))
    link = SingleLineStr(validate=validate.Length(max=256), allow_none=True)
    learning_type = make_choice_field(max_len=256, values=choices.CourseType.values, allow_none=True)
    time_to_complete = fields.Str(required=False, validate=validate_time_to_complete)
    rating = fields.Str(required=False, allow_none=True)


class RecordLearningSchema(Schema):
    class Meta:
        ordered = True

    title = LearningTitleSingleLineStr(required=True)
    link = SingleLineStr(validate=validate.Length(max=256), allow_none=True)
    learning_type = make_choice_field(max_len=256, values=choices.CourseType.values, allow_none=True)
    # Validation for time fields in function below as complex
    time_to_complete_hours = fields.Str(required=False)
    time_to_complete_minutes = fields.Str(required=False)
    rating = fields.Str(required=False, allow_none=True)

    @validates_schema(skip_on_field_errors=False)
    def validate_time_fields(self, data, **kwargs):
        hours_value = data.get("time_to_complete_hours")
        minutes_value = data.get("time_to_complete_minutes")
        max_hours_error = f"The course should be less than {constants.HOURS_LIMIT} hours"
        errors_dictionary = {}

        hours_error_msg = get_error_message_for_integer_validation(
            hours_value, max=constants.HOURS_LIMIT, error_msg=HOURS_ERROR, error_msg_max=max_hours_error
        )
        minutes_error_msg = get_error_message_for_integer_validation(minutes_value, max=59, error_msg=MINUTES_ERROR)

        if hours_error_msg:
            errors_dictionary["time_to_complete_hours"] = hours_error_msg
        if minutes_error_msg:
            errors_dictionary["time_to_complete_minutes"] = minutes_error_msg
        if errors_dictionary:
            raise ValidationError(errors_dictionary)

        if (not hours_value) and (not minutes_value):
            raise ValidationError({"time_to_complete_hours": HOURS_ERROR, "time_to_complete_minutes": MINUTES_ERROR})


class MyDetailsSchema(Schema):
    class Meta:
        ordered = True

    department = fields.Str(
        required=True,
        validate=validate.OneOf([code for code, _ in Department.choices()]),
        error_messages={
            "required": "You must select a department",
        },
    )
    grade = fields.Str(
        required=True,
        validate=validate.OneOf(choices.Grade.values),
        error_messages={
            "required": "You must select a grade",
        },
    )
    profession = fields.Str(
        required=True,
        validate=validate.OneOf(choices.Profession.values),
        error_messages={
            "required": "You must select a profession",
        },
    )
