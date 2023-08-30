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
    departments,
    interface,
    models,
    schemas,
    special_course_handler,
    survey_handling,
    utils,
)
from .additional_learning import additional_learning
from .decorators import enforce_user_completes_pre_survey, login_required
from .email_handler import send_learning_record_email


def frozendict(*args, **kwargs):
    return types.MappingProxyType(dict(*args, **kwargs))


page_compulsory_field_map = {
    "record-learning": ("title",),
}

# TODO: Finalise mandatory question list
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
}


missing_item_errors = {
    "title": "Please provide a title for this course",
}


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_pre_survey
def homepage_view(request):
    user = request.user
    use_streamlined_view = user.department in constants.DEPARTMENTS_USING_INTRANET_LINKS.keys()
    errors = {}
    selected_level = user.determine_competency_level()
    if selected_level:
        selected_level_course_title = special_course_handler.competency_level_courses[selected_level]
    else:
        selected_level = ""
        selected_level_course_title = ""
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
        selected_level_course = ""
    data = {
        "time_completed": time_completed,
        "selected_level": selected_level,
        "selected_level_course": selected_level_course,
        "all_level_courses": all_level_courses_information,
        "completed_feedback_survey": completed_feedback_survey,
        "streamlined_version": use_streamlined_view,
    }
    if use_streamlined_view:
        intranet_link = constants.DEPARTMENTS_USING_INTRANET_LINKS[user.department]
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


@login_required
@require_http_methods(["GET", "POST"])
@enforce_user_completes_pre_survey
class RecordLearningView(utils.MethodDispatcher):
    time_errors_map = {
        "time_to_complete_hours": "Please enter the hours this course took to complete e.g. 2",
        "time_to_complete_minutes": "Please enter the minutes this course took to complete, between 1 and 59",
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
        if user.department in constants.DEPARTMENTS_USING_INTRANET_LINKS.keys():
            template_name = "streamlined-record-learning.html"
        else:
            template_name = "record-learning.html"
        time_completed = user.get_time_completed()
        completed_obt = time_completed >= settings.REQUIRED_LEARNING_TIME
        learning_types = choices.CourseType.choices
        courses = models.Learning.objects.filter(user=user)
        data = {
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
                    if int(data["time_to_complete_minutes"]) > 59:
                        errors = {
                            **errors,
                            "time_to_complete_minutes": self.time_errors_map["time_to_complete_minutes"],
                        }
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
        if user.department in constants.DEPARTMENTS_USING_INTRANET_LINKS.keys():
            template_name = "streamlined-record-learning.html"
        else:
            template_name = "record-learning.html"
        course_schema = schemas.CourseSchema(unknown=marshmallow.EXCLUDE)
        manipulated_data = {
            "title": data["title"],
            "time_to_complete": str(
                (int(data["time_to_complete_hours"]) * 60) + int((data["time_to_complete_minutes"]))
            ),
            "link": data.get("link"),
            "learning_type": data.get("learning_type", None),
            "rating": data.get("rating", None),
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
                "rating": manipulated_data.get("rating", None),
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
            template_name=template_name,
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
@enforce_user_completes_pre_survey
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
@enforce_user_completes_pre_survey
def send_learning_record_view(request):
    user = request.user
    streamlined_department = user.department in constants.DEPARTMENTS_USING_INTRANET_LINKS.keys()
    courses = models.Learning.objects.filter(user=user)
    data = {
        "courses": courses,
        "streamlined_department": streamlined_department,
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
@enforce_user_completes_pre_survey
def check_delete_learning_view(request, learning_id):
    if request.method == "POST":
        if "delete-learning" in request.POST:
            interface.api.learning.delete(user_id=request.user.id, learning_id=learning_id)
        return redirect("record-learning")
    return render(request, "delete-learning-check.html")


@login_required
@require_http_methods(["POST"])
@enforce_user_completes_pre_survey
def delete_learning_view(request, learning_id):
    interface.api.learning.delete(user_id=request.user.id, learning_id=learning_id)
    return redirect("record-learning")


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_pre_survey
def additional_learning_view(request):
    additional_learning_records = additional_learning
    data = {
        "additional_learning": additional_learning_records,
    }
    return render(request, "additional-learning.html", {"data": data})


class RegisterView(utils.MethodDispatcher):
    template_name = "register.html"
    error_message = "Something has gone wrong.  Please try again."

    def error(self, request):
        messages.error(request, self.error_message)
        return render(request, self.template_name)

    def get(self, request, errors=None, data=None):
        department_choices = departments.Department.choices
        context = {
            "departments": department_choices,
            "grades": choices.Grade.choices,
            "professions": choices.Profession.choices,
            "errors": errors or {},
            "data": data or {},
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        department = request.POST.get("department")
        grade = request.POST.get("grade")
        profession = request.POST.get("profession")

        if not department or not grade or not profession:
            errors = {}
            if not department:
                messages.error(request, "You must select a department.")
                errors["department"] = "You must select a department"
            if not grade:
                messages.error(request, "You must select a grade.")
                errors["grades"] = "You must select a grade"
            if not profession:
                messages.error(request, "You must select a profession.")
                errors["professions"] = "You must select a profession"
            return self.get(request, errors, data=request.POST.dict())
        else:
            user.department = department
            user.grade = grade
            user.profession = profession
            user.save()

            return redirect(reverse("questions", args=("pre",)))


# Don't enforce user completes pre survey as this is the page to redirect to
@login_required
@require_http_methods(["GET"])
def intro_to_pre_survey_view(request):
    number_questions = len(survey_handling.questions_data["pre"])
    return render(request, "intro-pre-survey.html", {"number_questions": number_questions})


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_pre_survey
def end_pre_survey_view(request):
    return render(request, "end-pre-survey.html", {})


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_pre_survey
def intro_to_post_survey_view(request):
    return render(request, "intro-post-survey.html", {})


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_pre_survey
def end_post_survey_view(request):
    return render(request, "end-post-survey.html", {})


@login_required
@require_http_methods(["GET"])
@enforce_user_completes_pre_survey
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
