import os
import types

import marshmallow
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from . import (
    choices,
    interface,
    models,
    schemas,
    special_course_handler,
    survey_handling,
    utils,
)
from .email_handler import send_learning_record_email
from .utils import enforce_user_completes_pre_survey


def frozendict(*args, **kwargs):
    return types.MappingProxyType(dict(*args, **kwargs))


page_compulsory_field_map = {
    "record-learning": ("title",),
}

missing_item_errors = {
    "title": "Please provide a title for this course",
}


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_pre_survey()
def index_view(request):
    return redirect(reverse("homepage"))


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_pre_survey()
def homepage_view(request):
    user = request.user
    errors = {}
    survey_answer = models.SurveyResult.objects.get(user=user, survey_type="pre", page_number=1)
    selected_level = survey_answer.data["competency"]
    recommended_course_title = special_course_handler.competency_level_courses[selected_level]
    recommended_course = special_course_handler.get_special_course_information(recommended_course_title)
    extra_recommended_course_titles = [
        value
        for key, value in special_course_handler.competency_level_courses.items()
        if value != recommended_course_title
    ]
    extra_recommended_courses = [
        special_course_handler.get_special_course_information(course_title)
        for course_title in extra_recommended_course_titles
    ]
    extra_recommended_courses_information = [
        {
            "title": extra_course.title,
            "link": extra_course.link,
            "id": extra_course.id,
            "is_complete": user.has_completed_course(extra_course.id),
        }
        for extra_course in extra_recommended_courses
    ]
    recommended_course_information = {
        "title": recommended_course.title,
        "link": recommended_course.link,
        "id": recommended_course.id,
        "is_complete": user.has_completed_course(recommended_course.id),
    }
    team_meeting_course = special_course_handler.get_special_course_information(
        special_course_handler.team_meeting_course_title
    )
    time_completed = user.get_time_completed()
    data = {
        "time_completed": time_completed,
        "recommended_course": recommended_course_information,
        "extra_recommended_courses": extra_recommended_courses_information,
        "team_meeting_course": team_meeting_course,
    }
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
@enforce_user_completes_pre_survey()
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
@require_http_methods(["GET", "POST"])
@enforce_user_completes_pre_survey()
class RecordLearningView(utils.MethodDispatcher):
    time_errors_map = {
        "time_to_complete_hours": "Please enter the hours this course took to complete e.g. 2",
        "time_to_complete_minutes": "Please enter the minutes this course took to complete e.g. 45",
    }

    def get(
        self,
        request,
        course_id=None,
        data=None,
        errors=None,
    ):
        if not errors:
            errors = {}
        if not data:
            data = {}
        user = request.user
        time_completed = user.get_time_completed()
        learning_types = choices.CourseType.choices
        courses = models.Learning.objects.filter(user=user)
        data = {
            "time_completed": time_completed,
            "learning_types": learning_types,
            "courses": courses,
        }
        if course_id:
            course = models.Course.objects.filter(pk=course_id).first()
            if course:
                data = {
                    **data,
                    "title": course.title,
                    "learning_type": course.learning_type or "",
                    "time_to_complete_minutes": course.time_to_complete % 60,
                    "time_to_complete_hours": course.time_to_complete // 60,
                    "link": course.link or "",
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

    def post(self, request, course_id=None):
        data = request.POST.dict()
        errors = validate(request, "record-learning", data)
        if not data["time_to_complete_hours"] and not data["time_to_complete_minutes"]:
            errors = {
                **errors,
                "time_to_complete_minutes": self.time_errors_map["time_to_complete_minutes"],
                "time_to_complete_hours": self.time_errors_map["time_to_complete_hours"],
            }
        if errors:
            return self.get(request, data=data, errors=errors)
        if data["time_to_complete_hours"] or data["time_to_complete_minutes"]:
            if data["time_to_complete_hours"]:
                try:
                    value = int(data["time_to_complete_hours"])
                    if value < 0:
                        raise ValueError
                except ValueError:
                    errors = {
                        **errors,
                        "time_to_complete_hours": self.time_errors_map["time_to_complete_hours"],
                    }
            else:
                data["time_to_complete_hours"] = 0
            if data["time_to_complete_minutes"]:
                try:
                    value = int(data["time_to_complete_minutes"])
                    if value < 0:
                        raise ValueError
                except ValueError:
                    errors = {
                        **errors,
                        "time_to_complete_minutes": self.time_errors_map["time_to_complete_minutes"],
                    }
            else:
                data["time_to_complete_minutes"] = 0
        if errors:
            return self.get(request, data=data, errors=errors)
        user = request.user
        course_schema = schemas.CourseSchema(unknown=marshmallow.EXCLUDE)
        manipulated_data = {
            "title": data["title"],
            "time_to_complete": str(
                (int(data["time_to_complete_hours"]) * 60) + int((data["time_to_complete_minutes"]))
            ),
            "link": data.get("link"),
            "learning_type": data.get("learning_type", None),
        }
        try:
            course_schema.load(manipulated_data, partial=True)
        except marshmallow.exceptions.ValidationError as err:
            errors = dict(err.messages)
        else:
            learning_data = {
                "title": manipulated_data.get("title", None),
                "link": manipulated_data.get("link", None),
                "learning_type": manipulated_data.get("learning_type", None),
                "time_to_complete": manipulated_data.get("time_to_complete", None),
            }
            _ = interface.api.learning.create(user.id, user.id, learning_data, course_id)
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
@enforce_user_completes_pre_survey()
@require_http_methods(["GET"])
def complete_hours_view(request):
    user = request.user
    if user.has_completed_required_time():
        user.has_marked_complete = True
        user.save()
        if not user.has_completed_post_survey:
            return redirect("questions", "post")
        return redirect("record-learning")
    else:
        messages.info(request, "You have not completed the required hours, please try again.")
        return redirect("record-learning")


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_pre_survey()
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
    survey_type = survey_type
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
    survey_type = survey_type
    errors, data = clean_data(page_number, survey_type, data, validate=False)
    if errors:
        return questions_view_get(request, survey_type, page_number, errors=errors)
    else:
        save_data(survey_type, request.user, page_number, data)
    if page_number >= len(survey_handling.questions_data[survey_type]):
        if survey_type == "post":
            completed_post_survey = models.SurveyResult.objects.filter(
                page_number=1, survey_type=survey_type, user=request.user
            ).first()
            if completed_post_survey:
                completed_level = completed_post_survey.data["training-level"]
                return redirect("questions", completed_level)
        setattr(request.user, f"has_completed_{survey_handling.survey_completion_map[survey_type]}_survey", True)
        request.user.save()
        return redirect("homepage")
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
    question_ids = tuple(q["id"] for q in section["questions"] if q["answer_type"] != "checkboxes")
    list_question_ids = tuple(q["id"] for q in section["questions"] if q["answer_type"] == "checkboxes")
    if validate:
        errors = {qid: "Please answer this question" for qid in question_ids if qid not in data}
    else:
        errors = {}
    context = {k: data.get(k, "") for k in question_ids}
    context = {k: data.getlist(k, "") for k in list_question_ids} | context
    return errors, context


def save_data(survey_type, user, page_number, data):
    if models.SurveyResult.objects.filter(survey_type=survey_type, user=user, page_number=page_number).exists():
        item = models.SurveyResult.objects.get(survey_type=survey_type, user=user, page_number=page_number)
    else:
        item = models.SurveyResult(survey_type=survey_type, user=user, page_number=page_number)
    item.data = data
    item.save()
    return item


@login_required
@require_http_methods(["GET", "POST"])
@enforce_user_completes_pre_survey()
def send_learning_record_view(request):
    user = request.user
    courses = models.Learning.objects.filter(user=user)
    data = {
        "courses": courses,
    }
    errors = {}
    if request.method == "POST":
        email_validator = EmailValidator()
        email_address = request.POST.get("email")
        try:
            email_validator(email_address)
            send_learning_record_email(user)
            data = {
                "successfully_sent": True,
                "sent_to": email_address,
            } | data
            return render(
                request, "email-learning-record.html", context={"request": request, "data": data, "errors": errors}
            )
        except ValidationError:
            errors = {"email": "Please enter a valid email address"}
            return render(
                request, "email-learning-record.html", context={"request": request, "data": data, "errors": errors}
            )
    else:
        return render(
            request, "email-learning-record.html", context={"request": request, "data": data, "errors": errors}
        )


@login_required
@require_http_methods(["POST"])
@enforce_user_completes_pre_survey()
def remove_learning_view(request, learning_id):
    interface.api.learning.delete(user_id=request.user.id, learning_id=learning_id)
    return redirect("record-learning")


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_pre_survey()
def download_learning_view(request):
    file_name = settings.SELF_REFLECTION_FILENAME
    filepath = os.path.join(settings.STATICFILES_DIRS[0], file_name)

    if os.path.exists(filepath):
        with open(filepath, "rb") as worddoc:  # read as binary
            content = worddoc.read()  # Read the file
            response = HttpResponse(
                content, content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            response["Content-Disposition"] = f"attachment; filename={file_name}"
            response["Content-Length"] = len(content)  # calculate length of content
            return response
    else:
        return HttpResponse("File not found", status=404)
