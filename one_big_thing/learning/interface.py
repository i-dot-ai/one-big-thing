import marshmallow

from . import models, schemas
from .utils import Entity, Facade, register_event, with_schema


class CreateCourseSchema(marshmallow.Schema):
    data = marshmallow.fields.Nested(schemas.CourseSchema)


class Course(Entity):
    @with_schema(load=CreateCourseSchema, dump=schemas.CourseSchema)
    @register_event("Course created")
    def create(self, data):
        course = models.Course()
        for key, value in data.items():
            setattr(course, key, value)
        course.save()
        return course


facade = Facade(course=Course())
