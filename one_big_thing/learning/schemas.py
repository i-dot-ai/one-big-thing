from marshmallow import Schema, ValidationError, fields, validate

from one_big_thing.learning.utils import is_civil_service_email

from . import choices, constants
from one_big_thing.learning.departments import Department


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
        none_error_msg = kwargs.get("none_error_msg")
        if none_error_msg:
            raise ValidationError(none_error_msg)
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


def make_choice_field(max_len, values, allow_none=False, required=False, **kwargs):
    if allow_none:
        field = SingleLineStr(
            validate=validate.And(validate.Length(max=max_len), validate_choice_and_length_or_none(values)),
            allow_none=True,
            required=required,
            **kwargs,
        )
    else:
        field = SingleLineStr(validate=validate.And(validate.Length(max=max_len), validate.OneOf(values)), required=required, **kwargs)
    return field


class UserSchema(Schema):
    email = fields.Str(validate=validate_email)


class TimeStampedModelSchema(Schema):
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)


class UUIDPrimaryKeyBaseModelSchema(Schema):
    id = fields.UUID()


def validate_positive_integer(value, max=None, error_msg="There is an error with this value", error_msg_max=""):
    """
    Checks if value is a positive integer, optionally checks if below max.

    Args:
        value: Any value to be validated
        max: Optional value to check value is below max
        error_msg (str): General error message to display
        error_msg_max (str): Optional error message if number exceeds max, otherwise error_msg is displayed
    """
    try:
        value = int(value)
        if value < 0:
            raise ValidationError(error_msg)
        elif max and (value > max):
            if error_msg_max:
                raise ValidationError(error_msg_max)
            raise ValidationError(error_msg)
    except ValueError:
        raise ValidationError(error_msg)


def validate_time_to_complete(value):
    validate_positive_integer(value, error_msg="Please enter the time this course took to complete in minutes, e.g. 15")


def validate_time_to_complete_hours(value):
    general_error = "Please enter the hours this course took to complete, for example, 2"
    max_hours_error = f"The course should be less than {constants.HOURS_LIMIT} hours"
    validate_positive_integer(value, max=constants.HOURS_LIMIT, error_msg=general_error, error_msg_max=max_hours_error)


def validate_time_to_complete_minutes(value):
    minutes_error = "Please enter the minutes this course took to complete, between 0 and 59"
    validate_positive_integer(value, max=59, error_msg=minutes_error)


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
    title = LearningTitleSingleLineStr(required=True)
    link = SingleLineStr(validate=validate.Length(max=256), allow_none=True)
    learning_type = make_choice_field(max_len=256, values=choices.CourseType.values, allow_none=True)
    time_to_complete_hours = fields.Str(required=False, validate=validate_time_to_complete_hours)
    time_to_complete_minutes = fields.Str(validate=validate_time_to_complete_minutes)
    rating = fields.Str(required=False, allow_none=True)


class MyDetailsSchema(Schema):
    # department = make_choice_field(max_len=254, values=Department.values, required=True, none_error_msg="You must select a department")
    # grade = make_choice_field(max_len=254, values=choices.Grade.values, required=True, none_error_msg="You must select a grade")
    # profession = make_choice_field(max_len=254, values=choices.Profession.values, required=True, none_error_msg="You must select a profession")
    department = fields.Str(
        required=True,
        validate=validate.OneOf(Department.values),
        error_messages={
            'required': "You must select a department",
        }
    )
    grade = fields.Str(
        required=True,
        validate=validate.OneOf(choices.Grade.values),
        error_messages={
            'required': "You must select a grade",
         }
    )
    profession = fields.Str(
        required=True,
        validate=validate.OneOf(choices.Profession.values),
        error_messages={
            'required': "You must select a profession", 
        }
    )