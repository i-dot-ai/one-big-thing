import marshmallow
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from . import choices, interface, models, schemas, utils

page_compulsory_field_map = {
    "record-learning": (
        "title",
        "time_to_complete",
    ),
}

missing_item_errors = {
    "title": "Please provide a title for this course",
    "time_to_complete": "Please enter the time this course took to complete in minutes, e.g. 15",
}


@login_required
@require_http_methods(["GET"])
def index_view(request):
    return redirect(reverse("homepage"))


@login_required
@require_http_methods(["GET"])
def homepage_view(request):
    data = {}
    errors = {}
    return render(
        request,
        template_name="homepage.html",
        context={
            "request": request,
            "data": data,
            "errors": errors,
        },
    )


@login_required
@require_http_methods(["GET"])
def test_view(request):
    courses = models.Course.objects.all()
    data = {"courses": courses}
    errors = {}
    return render(
        request,
        template_name="test.html",
        context={
            "request": request,
            "data": data,
            "errors": errors,
        },
    )


class RecordLearningView(utils.MethodDispatcher):
    def get(
        self,
        request,
        data=None,
        errors=None,
    ):
        if not errors:
            errors = {}
        if not data:
            # _ = interface.api.session.get_answer(session_id, page_name) # TODO: Replace with call to get course data
            data = {}
        user = request.user
        time_completed = user.get_time_completed()
        learning_types = choices.CourseType.choices
        courses = models.Course.objects.filter(completion__user=user)
        data = {
            "time_completed": time_completed,
            "learning_types": learning_types,
            "courses": courses,
        }
        return render(
            request,
            template_name="record-learning.html",
            context={
                "request": request,
                "data": data,
                "errors": errors,
            },
        )

    def post(self, request):
        data = request.POST.dict()
        # data = {key: value for key, value in data.items() if value }
        errors = validate(request, "record-learning", data)
        if errors:
            return self.get(request, data=data, errors=errors)
        user = request.user
        course_schema = schemas.CourseSchema(unknown=marshmallow.EXCLUDE)
        try:
            serialized_course = course_schema.load(data, partial=True)
        except marshmallow.exceptions.ValidationError as err:
            errors = dict(err.messages)
        else:
            course = interface.api.course.create(serialized_course)
            _ = interface.api.completion.create(user.id, course["id"], user.id)
            return redirect(
                "record-learning"
            )  # TODO: Use class get to show success message when creating course instead of using redirect
        time_completed = user.get_time_completed()
        learning_types = choices.CourseType.choices
        data = {"time_completed": time_completed, "learning_types": learning_types, **data}
        return render(
            request,
            template_name="record-learning.html",
            context={
                "request": request,
                "data": data,
                "errors": errors,
            },
        )


def validate(request, page_name, data):
    fields = page_compulsory_field_map.get(page_name, ())
    missing_fields = tuple(field for field in fields if not data.get(field))
    errors = {field: missing_item_errors[field] for field in missing_fields}
    return errors
