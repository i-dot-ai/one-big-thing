import marshmallow

from . import models, schemas
from .utils import Entity, Interface, register_event, with_schema


class CreateCourseSchema(marshmallow.Schema):
    data = marshmallow.fields.Nested(schemas.CourseSchema)


class CreateLearningSchema(marshmallow.Schema):
    user_id = marshmallow.fields.UUID()
    course_id = marshmallow.fields.UUID(allow_none=True)
    data = marshmallow.fields.Nested(schemas.LearningSchema)
    user_to_add = marshmallow.fields.UUID()


class CreateLearningResponseSchema(marshmallow.Schema):
    learning_id = marshmallow.fields.UUID()


class CreateFeedbackSchema(marshmallow.Schema):
    user_id = marshmallow.fields.UUID()
    data = marshmallow.fields.Nested(schemas.FeedbackSchema)
    user_to_add = marshmallow.fields.UUID()


class CreateFeedbackResponseSchema(marshmallow.Schema):
    feedback_id = marshmallow.fields.UUID()


class DeleteLearningSchema(marshmallow.Schema):
    user_id = marshmallow.fields.UUID()
    learning_id = marshmallow.fields.UUID()


class DeleteLearningSchemaResponse(marshmallow.Schema):
    user_id = marshmallow.fields.UUID()


class Course(Entity):
    @with_schema(load=CreateCourseSchema, dump=schemas.CourseSchema)
    @register_event("Course created")
    def create(self, data):
        course = models.Course()
        for key, value in data.items():
            setattr(course, key, value)
        course.save()
        return course


class Learning(Entity):
    @with_schema(load=CreateLearningSchema, dump=CreateLearningResponseSchema)
    @register_event("Learning created")
    def create(self, user_id, user_to_add, data, course_id=None):
        learning = models.Learning()
        user = models.User.objects.get(pk=user_to_add)
        for key, value in data.items():
            setattr(learning, key, value)
        if course_id:
            course = models.Course.objects.filter(pk=course_id).first()
            if course:
                learning.course = course
        learning.user = user
        learning.save()
        response = {"learning_id": learning.id}
        return response

    @with_schema(load=DeleteLearningSchema, dump=DeleteLearningSchemaResponse)
    @register_event("Deleted learning")
    def delete(self, user_id, learning_id):
        learning_record = models.Learning.objects.get(user__id=user_id, pk=learning_id)
        learning_record.delete()
        response = {"user_id": user_id}
        return response


class Feedback(Entity):
    @with_schema(load=CreateFeedbackSchema, dump=CreateFeedbackResponseSchema)
    @register_event("Feedback created")
    def create(self, user_id, user_to_add, data):
        feedback = models.Feedback()
        user = models.User.objects.get(pk=user_to_add)
        for key, value in data.items():
            setattr(feedback, key, value)
        feedback.user = user
        feedback.save()
        response = {"feedback_id": feedback.id}
        return response


api = Interface(course=Course(), learning=Learning(), feedback=Feedback())
