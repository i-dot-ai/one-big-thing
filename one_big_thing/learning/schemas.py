from marshmallow import Schema, ValidationError, fields, validate

from one_big_thing.learning.utils import is_civil_service_email

from . import choices


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


def validate_time_to_complete(value):
    try:
        _ = int(value)
    except ValueError:
        raise ValidationError("Please enter the time this course took to complete in minutes, e.g. 15")


class CourseSchema(TimeStampedModelSchema):
    title = SingleLineStr(required=True, validate=validate.Length(max=1024))
    link = SingleLineStr(validate=validate.Length(max=256), allow_none=True)
    learning_type = make_choice_field(max_len=256, values=choices.CourseType.values, allow_none=True)
    time_to_complete = fields.Str(required=True, validate=validate_time_to_complete)
    # strengths = fields.Str()  # Figure out if we're using these or not
