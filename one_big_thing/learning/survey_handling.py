import yaml
from django.conf import settings

with (settings.BASE_DIR / "pre_questions.yaml").open() as f:
    pre_questions_data = yaml.safe_load(f)

with (settings.BASE_DIR / "post_questions.yaml").open() as f:
    post_questions_data = yaml.safe_load(f)

_competencies = (
    ("beginner", "Beginner"),
    ("intermediate", "Intermediate"),
    ("expert", "Expert"),
)

competencies = tuple({"label": label, "name": name} for (label, name) in _competencies)
pre_questions = tuple(q for section in pre_questions_data for q in section["questions"])
post_questions = tuple(q for section in pre_questions_data for q in section["questions"])
all_questions = tuple(*pre_questions, *post_questions)
section_pre_questions_map = {
    section["title"]: tuple(question["id"] for question in section["questions"]) for section in pre_questions
}
section_post_questions_map = {
    section["title"]: tuple(question["id"] for question in section["questions"]) for section in post_questions
}
section_all_questions_map = {
    **section_pre_questions_map,
    **section_post_questions_map,
}

answer_labels = {
    "agree-1-5": {
        "1": "Strongly disagree",
        "2": "Disagree",
        "3": "Neither agree nor disagree",
        "4": "Agree",
        "5": "Strongly agree",
    },
    "rating-1-5": {"1": "Poor", "2": "Fair", "3": "Good", "4": "Very good", "5": "Excellent"},
    "competency": dict(_competencies),
}

agree_pre_questions = tuple(item["id"] for item in pre_questions if item["answer_type"] == "agree-1-5")
agree_post_questions = tuple(item["id"] for item in post_questions if item["answer_type"] == "agree-1-5")
competency_labels = tuple(item["label"] for item in competencies)
pre_question_sections = tuple(item["title"] for item in pre_questions_data if item["title"] != "Competency")
post_question_sections = tuple(item["title"] for item in post_questions_data if item["title"] != "Competency")
all_question_sections = tuple(*pre_question_sections, *post_question_sections)


def get_competency_name(competency_label):
    matching = [item["name"] for item in competencies if item["label"] == competency_label]
    if not matching:
        return None
    return matching[0]


def get_question(question_number):
    matching = [item["text"] for item in all_questions if item["id"] == question_number]
    if not matching:
        return None
    return matching[0]


def get_question_ids_for_section(section):
    return section_all_questions_map[section]


# Excludes team
section_map = {k: get_question_ids_for_section(k) for k in all_question_sections}
