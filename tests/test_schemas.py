from marshmallow import Schema, ValidationError
from nose.tools import assert_raises_regexp, with_setup

from one_big_thing.learning import choices, models, schemas

from .utils import with_authenticated_client


class MadeUpSchema(Schema):
    string_field = schemas.SingleLineStr(allow_none=True)
    choice_field_one = schemas.make_choice_field(max_len=50, values=choices.CourseType.values, allow_none=True)
    choice_field_two = schemas.make_choice_field(max_len=50, values=choices.CourseType.values, allow_none=False)


def test_date_and_blank_field():
    schema = MadeUpSchema()
    deserialized_obj = schema.load({"string_field": "example string"})
    assert deserialized_obj["string_field"] == "example string"
    deserialized_obj = schema.load({"string_field": None})
    assert deserialized_obj["string_field"] is None


# Don't always want schemas to match, but we do for some models
def check_schema_model_match_fields(model_name, schema_name, related_fields_to_ignore={"learning"}):
    model = getattr(models, model_name)
    schema = getattr(schemas, schema_name)
    model_field_names = {f.name for f in model._meta.get_fields()}
    model_field_names_to_include = model_field_names.difference(related_fields_to_ignore)
    schema_field_names = set(schema._declared_fields.keys())
    assert schema_field_names == model_field_names_to_include, model_field_names_to_include.difference(
        schema_field_names
    )


def test_course_schema_has_relevant_fields():
    check_schema_model_match_fields(model_name="Course", schema_name="CourseSchema")


def setup_course():
    new_course = models.Course(title="Test course schemas", time_to_complete="120")
    new_course.save()
    # TODO - add more fields
    new_course.save()


def teardown_course():
    course = models.Course.objects.get(title="Test course schemas")
    course.delete()


@with_setup(setup_course, teardown_course)
@with_authenticated_client
def test_course_schema_dump(client):
    course_schema = schemas.CourseSchema()
    course = models.Course.objects.get(title="Test course schemas")
    serialized_course = course_schema.dump(course)
    assert serialized_course


def test_course_schema():
    course_schema = schemas.CourseSchema()
    # TODO - should really have more fields, and nested fields!
    valid_data = {
        "title": "My first course",
        "link": "https://google.co.uk/",
        "learning_type": choices.CourseType.VIDEO.value,
        "time_to_complete": "120",
    }
    invalid_course_type = {
        "title": "Title",
        "time_to_complete": "Invalid time",
    }
    assert course_schema.load(valid_data)
    error_message = ""
    try:
        course_schema.load(invalid_course_type)
    except ValidationError as e:
        error_message = e.messages["time_to_complete"][0]
    assert error_message == "Please enter the time this course took to complete in minutes, e.g. 15"


def test_user_schema():
    user_schema = schemas.UserSchema()
    error_message = ""
    try:
        user_schema.load({"email": "invalid@example.net"})
    except ValidationError as e:
        error_message = e.messages["email"][0]
    assert error_message == "This should be a valid Civil Service email", error_message
    try:
        user_schema.load({"email": "p"})
    except ValidationError as e:
        error_message = e.messages["email"][0]
    assert error_message == "This should be a valid Civil Service email", error_message


def test_make_choice_field():
    schema = MadeUpSchema()
    deserialized_obj = schema.load(
        {"string_field": "valid string", "choice_field_one": "", "choice_field_two": "WRITTEN_RESOURCE"}
    )
    assert deserialized_obj["string_field"] == "valid string"
    assert deserialized_obj["choice_field_one"] == ""
    assert deserialized_obj["choice_field_two"] == "WRITTEN_RESOURCE"
    try:
        deserialized_obj = schema.load(
            {"string_field": "valid string", "choice_field_one": "WRITTEN_RESOURCE", "choice_field_two": ""}
        )
    except ValidationError as e:
        error_message = e.messages["choice_field_two"][0]
        assert "Must be one of: WRITTEN_RESOURCE" in error_message, error_message
    try:
        deserialized_obj = schema.load(
            {"string_field": "invalid string\n has a newline", "choice_field_one": "bob", "choice_field_two": "VIDEO"}
        )
    except ValidationError as e:
        error_message = e.messages["string_field"][0]
        assert "Cannot contain linebreaks" in error_message, error_message
    try:
        deserialized_obj = schema.load(
            {"string_field": "valid str", "choice_field_one": "bob", "choice_field_two": "VIDEO"}
        )
    except ValidationError as e:
        error_message = e.messages["choice_field_one"][0]
        assert "Must be one of: WRITTEN_RESOURCE" in error_message, error_message


def test_validate_time_to_complete_no_errors():
    schemas.validate_time_to_complete(15)
    schemas.validate_time_to_complete("87")
    schemas.validate_time_to_complete_minutes(59)
    schemas.validate_time_to_complete_minutes(0)
    schemas.validate_time_to_complete_hours(24)
    schemas.validate_time_to_complete_hours(200)


def test_validate_time_to_complete_errors():
    with assert_raises_regexp(ValidationError, "Please enter the time this course took to complete in minutes"):
        schemas.validate_time_to_complete("a long time")
    with assert_raises_regexp(ValidationError, "Please enter the time this course took to complete in minutes"):
        schemas.validate_time_to_complete(-9)


def test_validate_time_to_complete_hour_errors():
    with assert_raises_regexp(ValidationError, "Please enter the hours this course took to complete"):
        schemas.validate_time_to_complete_hours("a long time")
    with assert_raises_regexp(ValidationError, "The course should be less than 200 hours"):
        schemas.validate_time_to_complete_hours("18000")
    with assert_raises_regexp(ValidationError, "Please enter the hours this course took to complete"):
        schemas.validate_time_to_complete_hours(-3)


def test_validate_time_to_complete_minutes_errors():
    with assert_raises_regexp(ValidationError, "Please enter the minutes this course took to complete"):
        schemas.validate_time_to_complete_minutes(60)
    with assert_raises_regexp(ValidationError, "Please enter the minutes this course took to complete"):
        schemas.validate_time_to_complete_minutes("this is a string")
    with assert_raises_regexp(ValidationError, "Please enter the minutes this course took to complete"):
        schemas.validate_time_to_complete_minutes(-5)


def test_my_details_schema():
    my_details_schema = schemas.MyDetailsSchema()
    details_no_errors = my_details_schema.load(
        {"department": "cabinet-office", "grade": "GRADE7", "profession": "ANALYSIS"}
    )
    assert details_no_errors
    with assert_raises_regexp(ValidationError, "You must select a department"):
        my_details_schema.load({"grade": "HIGHER_EXECUTIVE_OFFICER", "profession": "ANALYSIS"})
    with assert_raises_regexp(ValidationError, "You must select a grade"):
        my_details_schema.load({"profession": "ANALYSIS"})
    with assert_raises_regexp(ValidationError, "You must select a profession"):
        my_details_schema.load({"grade": "HIGHER_EXECUTIVE_OFFICER"})
