pre_questions_data = [
    {
        "title": "Competency",
        "questions": [{"id": "competency", "text": "How well do you understand data topics?", "answer_type": "radio"}],
    },
    {
        "title": "Create a unifying experience and build a shared identity"
        " (or create a shared vision, define shared goals)",
        "questions": [
            {
                "id": "aims",
                "text": "I am aware of the aims of One Big Thing",
                "answer_type": "agree-1-7",
            },
            {
                "id": "shared-identity",
                "text": 'I feel a sense of "shared identity" with other civil servants',
                "answer_type": "agree-1-7",
            },
            {
                "id": "identity-is-important",
                "text": "My identity as a civil servant is important to me",
                "answer_type": "agree-1-7",
            },
        ],
    },
    {
        "title": "Uplift in data awareness",
        "questions": [
            {
                "id": "positive-day-to-day",
                "text": "I feel positive about using data in my day-to-day role",
                "answer_type": "agree-1-7",
            },
            {
                "id": "effective-day-to-day",
                "text": "I know how to use data effectively in my day-to-day role",
                "answer_type": "agree-1-7",
            },
        ],
    },
]

post_questions_data = [
    {
        "title": "Training completed",
        "questions": [
            {
                "id": "training-level",
                "text": "Which level of training did you take part in?",
                "answer_type": "radio",
            }
        ],
    },
    {
        "title": "Create a unifying experience and build a shared identity",
        "questions": [
            {
                "id": "shared-identity",
                "text": 'I feel a sense of "shared identity" with other civil servants',
                "answer_type": "agree-1-7",
            },
            {
                "id": "own-identity",
                "text": "My identity as a civil servant is important to me",
                "answer_type": "agree-1-7",
            },
        ],
    },
    {
        "title": 'Following "One Big Thing", '
        "please rate how much you agree or disagree with each of the following statements:",
        "questions": [
            {
                "id": "confident",
                "text": "I feel confident about using data in my day-to-day role",
                "answer_type": "agree-1-7",
            },
            {
                "id": "how-to-use-data",
                "text": "I know how to use data effectively in my day-to-day role",
                "answer_type": "agree-1-7",
            },
            {
                "id": "how-data-can-support",
                "text": "I am aware of how data can support my day-to-day role",
                "answer_type": "agree-1-7",
            },
        ],
    },
]

_competencies = (
    ("beginner", "Beginner"),
    ("intermediate", "Intermediate"),
    ("expert", "Expert"),
)

_training_levels = (
    ("awareness", "Awareness"),
    ("working", "Working"),
    ("practitioner", "Practitioner"),
    ("unknown", "Don't know"),
)

questions_data = {
    "pre": pre_questions_data,
    "post": post_questions_data,
}

competencies = tuple({"label": label, "name": name} for (label, name) in _competencies)
pre_questions = tuple(q for section in pre_questions_data for q in section["questions"])
post_questions = tuple(q for section in post_questions_data for q in section["questions"])
all_questions = pre_questions + post_questions
section_pre_questions_map = {
    section["title"]: tuple(question["id"] for question in section["questions"]) for section in pre_questions_data
}
section_post_questions_map = {
    section["title"]: tuple(question["id"] for question in section["questions"]) for section in post_questions_data
}
section_all_questions_map = {
    **section_pre_questions_map,
    **section_post_questions_map,
}

answer_labels = {
    "agree-1-7": {
        "1": "Totally disagree",
        "2": "Strongly disagree",
        "3": "Disagree",
        "4": "Neither agree nor disagree",
        "5": "Agree",
        "6": "Strongly agree",
        "7": "Totally agree",
    },
    "rating-1-5": {"1": "Poor", "2": "Fair", "3": "Good", "4": "Very good", "5": "Excellent"},
    "competency": dict(_competencies),
    "training-level": dict(_training_levels),
}

agree_pre_questions = tuple(item["id"] for item in pre_questions if item["answer_type"] == "agree-1-5")
agree_post_questions = tuple(item["id"] for item in post_questions if item["answer_type"] == "agree-1-5")
competency_labels = tuple(item["label"] for item in competencies)
pre_question_sections = tuple(item["title"] for item in pre_questions_data if item["title"] != "Competency")
post_question_sections = tuple(item["title"] for item in post_questions_data if item["title"] != "Competency")
all_question_sections = pre_question_sections + post_question_sections
