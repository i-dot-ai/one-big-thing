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


def test_get_error_message_for_integer_validation_valid_inputs():
    error = schemas.get_error_message_for_integer_validation("98")
    assert not error
    error = schemas.get_error_message_for_integer_validation(78)
    assert not error
    error = schemas.get_error_message_for_integer_validation(None)
    assert not error
    error = schemas.get_error_message_for_integer_validation(78, max=100, error_msg="error", error_msg_max="error max")
    assert not error
    error = schemas.get_error_message_for_integer_validation("", max=100)
    assert not error


def test_get_error_message_for_integer_validation_invalid_inputs():
    error = schemas.get_error_message_for_integer_validation("i")
    assert "There is an error with this value" in error
    error = schemas.get_error_message_for_integer_validation(3000, max=100, error_msg="error")
    assert error == "error", error
    error = schemas.get_error_message_for_integer_validation(-1)
    assert "There is an error with this value" in error
    error = schemas.get_error_message_for_integer_validation(
        3000, max=100, error_msg="error", error_msg_max="max error"
    )
    assert error == "max error", error


def test_record_learning_schema():
    learning_schema = schemas.RecordLearningSchema()
    valid = {
        "title": "A good title",
        "link": "",
        "learning_type": "",
        "time_to_complete_hours": "6",
        "time_to_complete_minutes": "",
        "rating": "",
    }
    errors = learning_schema.validate(valid)
    assert not errors
    valid = {
        "title": "A good title",
        "link": "http://example.com",
        "learning_type": "VIDEO",
        "time_to_complete_hours": "6",
        "time_to_complete_minutes": "30",
        "rating": "5",
    }
    errors = learning_schema.validate(valid)
    assert not errors
    invalid = {
        "title": "",
        "link": "",
        "learning_type": "",
        "time_to_complete_hours": "",
        "time_to_complete_minutes": "",
        "rating": "",
    }
    errors = learning_schema.validate(invalid)
    assert "title" in errors
    assert "link" not in errors
    assert "learning_type" not in errors
    assert errors["time_to_complete_hours"] == "Please enter the hours this course took to complete, for example, 2"
    assert (
        errors["time_to_complete_minutes"] == "Please enter the minutes this course took to complete, between 0 and 59"
    )
    assert "rating" not in errors
    invalid = {
        "title": "A data course",
        "link": "http://example.com",
        "learning_type": "",
        "time_to_complete_hours": "99999",
        "time_to_complete_minutes": "-1",
        "rating": "",
    }
    errors = learning_schema.validate(invalid)
    assert errors["time_to_complete_hours"] == "The course should be less than 200 hours"
    assert (
        errors["time_to_complete_minutes"] == "Please enter the minutes this course took to complete, between 0 and 59"
    )
    invalid = {
        "title": "A data course",
        "link": "http://example.com",
        "learning_type": "",
        "time_to_complete_hours": "-1",
        "time_to_complete_minutes": "some text",
        "rating": "",
    }
    errors = learning_schema.validate(invalid)
    assert errors["time_to_complete_hours"] == "Please enter the hours this course took to complete, for example, 2"
    assert (
        errors["time_to_complete_minutes"] == "Please enter the minutes this course took to complete, between 0 and 59"
    )
    invalid = {
        "title": "A data course",
        "link": "http://example.com",
        "learning_type": "",
        "time_to_complete_hours": "",
        "time_to_complete_minutes": "70",
        "rating": "",
    }
    errors = learning_schema.validate(invalid)
    assert "title" not in errors
    assert "time_to_complete_hours" not in errors
    assert (
        errors["time_to_complete_minutes"] == "Please enter the minutes this course took to complete, between 0 and 59"
    )


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


def test_record_learning_schema_validation_errors():
    record_learning_schema = schemas.RecordLearningSchema()
    data_no_errors = record_learning_schema.load({"title": "Data training", "time_to_complete_hours": "2"})
    assert data_no_errors
    data_no_errors = record_learning_schema.load({"title": "Data training", "time_to_complete_minutes": "25"})
    assert data_no_errors
    data_no_errors = record_learning_schema.load(
        {"title": "Data training", "time_to_complete_hours": "1", "time_to_complete_minutes": "25"}
    )
    assert data_no_errors
    with assert_raises_regexp(ValidationError, "Please enter the hours"):
        record_learning_schema.load({"title": "Hi", "link": "http://example.com"})
    with assert_raises_regexp(ValidationError, "Please enter the minutes"):
        record_learning_schema.load({"title": "Hi", "link": "http://example.com"})
    with assert_raises_regexp(ValidationError, "Please enter the minutes"):
        record_learning_schema.load({"title": "Hi", "link": "http://example.com", "time_to_complete_minutes": "string"})
