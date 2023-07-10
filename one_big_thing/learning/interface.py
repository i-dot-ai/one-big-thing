import marshmallow

from . import models, schemas
from .utils import Entity, Interface, register_event, with_schema


class CreateCourseSchema(marshmallow.Schema):
    data = marshmallow.fields.Nested(schemas.CourseSchema)


class CreateCompletionSchema(marshmallow.Schema):
    user_id = marshmallow.fields.UUID()
    course_id = marshmallow.fields.UUID()
    user_to_add = marshmallow.fields.UUID()


class CreateCompletionResponseSchema(marshmallow.Schema):
    completion_id = marshmallow.fields.UUID()


class Course(Entity):
    @with_schema(load=CreateCourseSchema, dump=schemas.CourseSchema)
    @register_event("Course created")
    def create(self, data):
        course = models.Course()
        for key, value in data.items():
            setattr(course, key, value)
        course.save()
        return course


class Completion(Entity):
    @with_schema(load=CreateCompletionSchema, dump=CreateCompletionResponseSchema)
    @register_event("Completion created")
    def create(self, user_id, course_id, user_to_add):
        completion = models.Completion()
        user = models.User.objects.get(pk=user_to_add)
        course = models.Course.objects.get(pk=course_id)
        completion.course = course
        completion.user = user
        completion.save()
        response = {"completion_id": completion.id}
        return response


api = Interface(course=Course(), completion=Completion())
