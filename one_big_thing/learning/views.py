import types

import marshmallow
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from . import choices, interface, models, schemas, survey_handling, utils


def frozendict(*args, **kwargs):
    return types.MappingProxyType(dict(*args, **kwargs))


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


@login_required
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


@login_required
@require_http_methods(["GET"])
def complete_hours_view(request):
    user = request.user
    if user.has_completed_required_time():
        user.has_marked_complete = True
        user.save()
        return redirect("record-learning")
    else:
        messages.info(request, "You have not completed the required hours, please try again.")
        return redirect("record-learning")


@login_required
@require_http_methods(["GET"])
def survey_completed_view(request):
    return render(request, "survey-completed.html", {})


@login_required
@require_http_methods(["GET", "POST"])
def questions_view(request, survey_type, page_number=1):
    if request.method == "GET":
        return questions_view_get(request, survey_type, page_number)
    elif request.method == "POST":
        return questions_view_post(request, survey_type, page_number)


def questions_view_get(request, survey_type, page_number, errors=frozendict()):
    survey_type = survey_type.lower()
    section = survey_handling.questions_data[survey_type][page_number - 1]
    data = get_data(request.user, survey_type, page_number)
    return render(
        request,
        template_name="questions.html",
        context={
            "request": request,
            "data": data,
            "section": section,
            "survey_type": survey_type,
            "competencies": survey_handling.competencies,
            "page_number": page_number,
            "errors": errors,
            "answer_labels": survey_handling.answer_labels,
        },
    )


def questions_view_post(request, survey_type, page_number, errors=frozendict()):
    data = request.POST
    survey_type = survey_type.lower()
    errors, data = clean_data(page_number, survey_type, data, validate=False)
    if errors:
        return questions_view_get(request, survey_type, page_number, errors=errors)
    else:
        save_data(survey_type, request.user, page_number, data)
    if page_number >= len(survey_handling.questions_data[survey_type]):
        return redirect("survey-completed")
    else:
        next_page_number = page_number + 1
        return redirect("questions", survey_type=survey_type, page_number=next_page_number)


def get_data(user, survey_type, page_number):
    if models.SurveyResult.objects.filter(survey_type=survey_type, user=user, page_number=page_number).exists():
        item = models.SurveyResult.objects.get(survey_type=survey_type, user=user, page_number=page_number)
        return item.data
    else:
        return {}


def clean_data(page_number, survey_type, data, validate=False):
    section = survey_handling.questions_data[survey_type][page_number - 1]
    question_ids = tuple(q["id"] for q in section["questions"])
    if validate:
        errors = {qid: "Please answer this question" for qid in question_ids if qid not in data}
    else:
        errors = {}
    data = {k: data.get(k, "") for k in question_ids}
    return errors, data


def save_data(survey_type, user, page_number, data):
    if models.SurveyResult.objects.filter(survey_type=survey_type, user=user, page_number=page_number).exists():
        item = models.SurveyResult.objects.get(survey_type=survey_type, user=user, page_number=page_number)
    else:
        item = models.SurveyResult(survey_type=survey_type, user=user, page_number=page_number)
    item.data = data
    item.save()
    return item
