import types

import marshmallow
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from . import (
    choices,
    constants,
    interface,
    models,
    schemas,
    special_course_handler,
    survey_handling,
    utils,
)
from .additional_learning import additional_learning
from .decorators import (
    enforce_user_completes_details_and_pre_survey,
    login_required,
)
from .email_handler import send_learning_record_email
from .models import Department


def frozendict(*args, **kwargs):
    return types.MappingProxyType(dict(*args, **kwargs))


survey_questions_compulsory_field_map = {
    "pre": {
        1: [
            "confident-in-decisions",
        ],
        2: [
            "confidence-graphic-survey",
        ],
        3: [
            "confidence-explaining-chart",
        ],
    },
    "post": {
        1: [
            "training-level",
        ]
    },
}


ratings = (
    {"value": "1", "text": "1 ★"},
    {"value": "2", "text": "2 ★★"},
    {"value": "3", "text": "3 ★★★"},
    {"value": "4", "text": "4 ★★★★"},
    {"value": "5", "text": "5 ★★★★★"},
)


selected_level_label_map = {
    constants.AWARENESS: "Level 1 - Awareness",
    constants.WORKING: "Level 2 - Working",
    constants.PRACTITIONER: "Level 3 - Practitioner",
}


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_details_and_pre_survey
def homepage_view(request):
    user = request.user
    errors = {}
    selected_level = user.determine_competency_level()
    if selected_level:
        selected_level_course_title = special_course_handler.competency_level_courses[selected_level]
        selected_level_label = selected_level_label_map[selected_level]
    else:
        selected_level = ""
        selected_level_course_title = ""
        selected_level_label = ""
    all_level_course_titles = list(special_course_handler.competency_level_courses.values())
    all_level_courses = [
        special_course_handler.get_special_course_information(course_title) for course_title in all_level_course_titles
    ]
    all_level_courses_information = [
        {
            "title": course.title,
            "link": course.link,
            "id": course.id,
            "is_complete": user.has_completed_course(course.id),
        }
        for course in all_level_courses
    ]
    time_completed = user.get_time_completed()
    completed_feedback_survey = user.has_completed_post_survey
    if selected_level:
        selected_level_course = [
            course for course in all_level_courses_information if course["title"] == selected_level_course_title
        ][0]
    else:
        selected_level_course = {"title": "", "link": ""}
    data = {
        "time_completed": time_completed,
        "selected_level": selected_level,
        "selected_level_label": selected_level_label,
        "selected_level_course": selected_level_course,
        "all_level_courses": all_level_courses_information,
        "completed_feedback_survey": completed_feedback_survey,
        "streamlined_version": user.department.url is not None,
    }
    if user.department.url:
        intranet_link = user.department.url
        data["intranet_link"] = intranet_link
        return render(
            request,
            template_name="streamlined-homepage.html",
            context={
                "request": request,
                "data": data,
                "errors": errors,
            },
        )

    return render(
        request,
        template_name="homepage.html",
        context={
            "request": request,
            "data": data,
            "errors": errors,
        },
    )


def transform_learning_record(data):
    time_to_complete_hours = data.get("time_to_complete_hours")
    time_to_complete_minutes = data.get("time_to_complete_minutes")
    if not time_to_complete_hours:
        time_to_complete_hours = 0
    else:
        time_to_complete_hours = int(time_to_complete_hours)
    if not time_to_complete_minutes:
        time_to_complete_minutes = 0
    else:
        time_to_complete_minutes = int(time_to_complete_minutes)
    time_to_complete_total = time_to_complete_hours * 60 + time_to_complete_minutes
    time_to_complete_total = str(time_to_complete_total)
    transformed_data = {
        "title": data.get("title"),
        "time_to_complete": time_to_complete_total,
        "link": data.get("link"),
        "learning_type": data.get("learning_type"),
        "rating": data.get("rating", None) or None,
    }
    return transformed_data


@login_required
@require_http_methods(["GET", "POST"])
@enforce_user_completes_details_and_pre_survey
class RecordLearningView(utils.MethodDispatcher):
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
        if user.department.url:
            template_name = "streamlined-record-learning.html"
        else:
            template_name = "record-learning.html"
        time_completed = user.get_time_completed()
        completed_obt = time_completed >= settings.REQUIRED_LEARNING_TIME
        learning_types = choices.CourseType.choices
        courses = models.Learning.objects.filter(user=user)
        data = {
            **data,
            "time_completed": time_completed,
            "learning_types": learning_types,
            "courses": courses,
            "completed_obt": completed_obt,
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
            template_name=template_name,
            context={
                "request": request,
                "data": data,
                "errors": errors,
                "ratings": ratings,
            },
        )

    def post(self, request, course_id=None):
        data = request.POST.dict()
        record_learning_schema = schemas.RecordLearningSchema(unknown=marshmallow.EXCLUDE)
        errors = record_learning_schema.validate(data, partial=False)
        if errors:
            return self.get(request, data=data, errors=errors)
        user = request.user
        learning_data = transform_learning_record(data)
        interface.api.learning.create(user.id, user.id, learning_data, course_id)
        return redirect(
            "record-learning"
        )  # TODO: Use class get to show success message when creating course instead of using redirect


@login_required
@enforce_user_completes_details_and_pre_survey
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
    is_final_page = (page_number >= len(survey_handling.questions_data[survey_type])) & (survey_type != "post")
    return render(
        request,
        template_name="questions.html",
        context={
            "request": request,
            "data": data,
            "section": section,
            "survey_type": survey_type,
            "page_number": page_number,
            "errors": errors,
            "answer_labels": survey_handling.answer_labels,
            "is_final_page": is_final_page,
        },
    )


def questions_view_post(request, survey_type, page_number, errors=frozendict()):
    data = request.POST
    survey_type = survey_type
    errors, data = clean_data(page_number, survey_type, data, validate=True)
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
        if survey_type == "pre":
            return redirect("end-pre-survey")
        elif survey_type != "post":  # will be one of the training levels
            return redirect("end-post-survey")
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
        errors = {
            qid: "Please answer this question"
            for qid in survey_questions_compulsory_field_map.get(survey_type, {}).get(page_number, {})
            if qid not in data
        }
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
@enforce_user_completes_details_and_pre_survey
def send_learning_record_view(request):
    user = request.user
    courses = models.Learning.objects.filter(user=user)
    data = {
        "courses": courses,
        "streamlined_department": user.department.url,
    }
    errors = {}
    if request.method == "POST":
        email_validator = EmailValidator()
        email_address = request.POST.get("email")
        try:
            email_validator(email_address)
            send_learning_record_email(user, email_address)
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
@require_http_methods(["GET", "POST"])
@enforce_user_completes_details_and_pre_survey
def check_delete_learning_view(request, learning_id):
    if request.method == "POST":
        if "delete-learning" in request.POST:
            interface.api.learning.delete(user_id=request.user.id, learning_id=learning_id)
        return redirect("record-learning")
    return render(request, "delete-learning-check.html")


@login_required
@require_http_methods(["POST"])
@enforce_user_completes_details_and_pre_survey
def delete_learning_view(request, learning_id):
    interface.api.learning.delete(user_id=request.user.id, learning_id=learning_id)
    return redirect("record-learning")


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_details_and_pre_survey
def additional_learning_view(request):
    additional_learning_records = additional_learning
    data = {
        "additional_learning": additional_learning_records,
    }
    return render(request, "additional-learning.html", {"data": data})


# This happens before pre_survey
@login_required
@require_http_methods(["POST", "GET"])
class MyDetailsView(utils.MethodDispatcher):
    template_name = "my-details.html"
    error_message = "Something has gone wrong. Please try again."
    my_details_schema = schemas.MyDetailsSchema(unknown=marshmallow.EXCLUDE)

    def error(self, request):
        messages.error(request, self.error_message)
        return render(request, self.template_name)

    def get(self, request, errors=None, data=None):
        user = request.user
        data = self.my_details_schema.dump(user)
        context = {
            "departments": Department.choices(),
            "grades": choices.Grade.choices,
            "professions": choices.Profession.choices,
            "errors": errors or {},
            "data": data or {},
            "completed": request.user.completed_personal_details,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        try:
            details = self.my_details_schema.load(request.POST)
            for k, v in details.items():
                setattr(user, k, v)
                user.save()
            if not user.has_completed_pre_survey:
                return redirect(reverse("questions", args=("pre",)))
            else:
                return redirect(reverse("homepage"))
        except marshmallow.exceptions.ValidationError as err:
            errors = dict(err.messages)
            for k, v in errors.items():
                errors[k] = v[0]
                messages.error(request, v[0])
            return self.get(request, errors, data=request.POST.dict())


@login_required
@require_http_methods(["GET"])
def intro_to_pre_survey_view(request):
    completed_personal_details = request.user.completed_personal_details
    if not completed_personal_details:
        return redirect("my-details")
    number_questions = len(survey_handling.questions_data["pre"])
    return render(request, "intro-pre-survey.html", {"number_questions": number_questions})


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_details_and_pre_survey
def end_pre_survey_view(request):
    return render(request, "end-pre-survey.html", {})


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_details_and_pre_survey
def intro_to_post_survey_view(request):
    return render(request, "intro-post-survey.html", {})


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_details_and_pre_survey
def end_post_survey_view(request):
    return render(request, "end-post-survey.html", {})


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_details_and_pre_survey
def department_links_view(request):
    data = {"dept_links": constants.ALL_INTRANET_LINKS}
    errors = {}
    return render(
        request,
        template_name="department-links.html",
        context={
            "request": request,
            "data": data,
            "errors": errors,
        },
    )
