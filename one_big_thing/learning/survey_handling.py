from one_big_thing.learning import choices

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

shared_level_questions_data = [
    {
        "title": "How likely are you to do the following?",
        "questions": [
            {"id": "create-development-plan", "text": "I will create a development plan", "answer_type": "likely-1-7"},
            {
                "id": "add-new-learning-to-development-plan",
                "text": "I will add a new area of learning to my development plan",
                "answer_type": "likely-1-7",
            },
            {
                "id": "book-related-training",
                "text": "I will book a related training course",
                "answer_type": "likely-1-7",
            },
            {"id": "find-mentor", "text": "I will find a mentor", "answer_type": "likely-1-7"},
        ],
    },
    {
        "title": "Please rate how much you agree or disagree that each component of the training was helpful",
        "questions": [
            {
                "id": "training-helped-learning",
                "text": "The online training helped my learning",
                "answer_type": "agree-1-7",
            },
            {
                "id": "conversations-helped-learning",
                "text": "Conversations with my team or line manager helped my learning",
                "answer_type": "agree-1-7",
            },
            {
                "id": "additional-resources-helped-learning",
                "text": "Additional learning resources helped my learning",
                "answer_type": "agree-1-7",
            },
        ],
    },
    {
        "title": "Were there any formats of additional training you found useful?",
        "questions": [
            {
                "id": "useful-learning-formats",
                "text": "",
                "answer_type": "checkboxes",
            },
        ],
    },
    {
        "title": "Please rate how much you agree or disagree with the below statements",
        "questions": [
            {
                "id": "obt-good-use-of-time",
                "text": "I felt that One Big Thing training was a good use of my time",
                "answer_type": "agree-1-7",
            },
            {
                "id": "improved-understanding-of-using-data",
                "text": "I have an improved understanding of how to use data in my day-to-day role",
                "answer_type": "agree-1-7",
            },
            {
                "id": "intend-to-participate-in-further-training",
                "text": "I intend to participate in further data training and initiatives",
                "answer_type": "agree-1-7",
            },
            {
                "id": "content-was-relevant-to-my-role",
                "text": "I felt the content was relevant to my role",
                "answer_type": "agree-1-7",
            },
            {
                "id": "intend-to-apply-learning-in-my-role",
                "text": "I intend to apply learning from this training as I go forward in my role",
                "answer_type": "agree-1-7",
            },
        ],
    },
    {
        "title": "Please rate how much you agree or disagree with the below statements",
        "questions": [
            {
                "id": "aware-of-aims",
                "text": "I am aware of the aims of One Big Thing",
                "answer_type": "agree-1-7",
            },
            {
                "id": "time-to-participate",
                "text": "I had the time to participate in One Big Thing during Autumn",
                "answer_type": "agree-1-7",
            },
        ],
    },
    {
        "title": "Further questions",
        "questions": [
            {
                "id": "what-went-well",
                "text": "What if anything, went well about the training?",
                "answer_type": "textarea",
                "max_length": 150,
            },
            {
                "id": "what-can-be-improved",
                "text": "Was there anything that could have been improved?",
                "answer_type": "textarea",
            },
        ],
    },
    {
        "title": "Would you be willing to take part in a follow-up discussion?",
        "questions": [
            {
                "id": "willing-to-follow-up",
                "text": "",
                "answer_type": "radio",
            },
        ],
    },
]

awareness_level_questions_data = [
    {
        "title": 'Following "One Big Thing", '
        "please rate how much you agree or disagree with each of the following statements:",
        "questions": [
            {
                "id": "I-understand-what-data-means",
                "text": "I have a better understanding of what data is",
                "answer_type": "agree-1-7",
            },
            {
                "id": "data-is-not-relevant-to-my-role",
                "text": "I do not think data is relevant to my role",
                "answer_type": "agree-1-7",
            },
            {
                "id": "better-understand-what-data-is-showing",
                "text": "I am better at understanding what data is showing",
                "answer_type": "agree-1-7",
            },
            {
                "id": "I-am-more-interested-in-data",
                "text": "I am more interested in working with data in my day-to-day role",
                "answer_type": "agree-1-7",
            },
            {
                "id": "more-confident-using-data-for-decisions",
                "text": "I am more confident to analyse data to influence decisions",
                "answer_type": "agree-1-7",
            },
            {
                "id": "more-confident-communicating-data-to-influence-decisions",
                "text": "I am more able to confidently communicate data findings to influence decisions",
                "answer_type": "agree-1-7",
            },
        ],
    },
    *shared_level_questions_data,
]

working_level_questions_data = [
    {
        "title": 'Following "One Big Thing", '
        "please rate how much you agree or disagree with each of the following statements:",
        "questions": [
            {
                "id": "I-understand-different-data-techniques",
                "text": "I understand better how different data analysis techniques can transform data into insights",
                "answer_type": "agree-1-7",
            },
            {
                "id": "I-understand-critically-assessing-data",
                "text": "I understand better how to critically assess data collection, "
                "analysis and the insights derived from it",
                "answer_type": "agree-1-7",
            },
            {
                "id": "I-know-visualising-data",
                "text": "I know more about visualising and presenting data in a clear and concise way",
                "answer_type": "agree-1-7",
            },
            {
                "id": "importance-of-evaluating-outcomes-of-data-informed-decisions",
                "text": "I have learned about the importance of evaluating the outcomes of data-informed-decisions",
                "answer_type": "agree-1-7",
            },
            {
                "id": "obt-knowledge-drives-change",
                "text": "I will do something differently as a result of knowledge gained from One Big Thing",
                "answer_type": "agree-1-7",
            },
        ],
    },
    *shared_level_questions_data,
]

practitioner_level_questions_data = [
    {
        "title": 'Following "One Big Thing", '
        "please rate how much you agree or disagree with each of the following statements:",
        "questions": [
            {
                "id": "more-effectively-communicate-data-insights-to-improve-decisions",
                "text": "I understand better how to communicate data "
                "insights more effectively to improve data-driven decision-making",
                "answer_type": "agree-1-7",
            },
            {
                "id": "use-data-to-develop-a-clear-narrative",
                "text": "I can more confidently use data to develop a clear narrative",
                "answer_type": "agree-1-7",
            },
            {
                "id": "committed-to-high-quality-data",
                "text": "I am more committed to ensuring high data quality",
                "answer_type": "agree-1-7",
            },
            {
                "id": "better-identify-weakening-data",
                "text": "I can better anticipate what will weaken data quality through the data lifecycle",
                "answer_type": "agree-1-7",
            },
            {
                "id": "understanding-ethics-for-data",
                "text": "I am more confident in my understanding of ethics in relation to data",
                "answer_type": "agree-1-7",
            },
            {
                "id": "obt-knowledge-drives-change",
                "text": "I will do something differently as a result of knowledge gained from One Big Thing",
                "answer_type": "agree-1-7",
            },
        ],
    },
    *shared_level_questions_data,
]

unknown_level_questions_data = [
    *shared_level_questions_data,
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
    "awareness": awareness_level_questions_data,
    "working": working_level_questions_data,
    "practitioner": practitioner_level_questions_data,
    "unknown": unknown_level_questions_data,
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
    "likely-1-7": {
        "1": "Very unlikely",
        "2": "Unlikely",
        "3": "Somewhat unlikely",
        "4": "Neither likely or unlikely",
        "5": "Somewhat likely",
        "6": "Likely",
        "7": "Very likely",
    },
    "competency": dict(_competencies),
    "training-level": dict(_training_levels),
    "useful-learning-formats": choices.CourseType.mapping,
    "willing-to-follow-up": choices.YesNo.mapping,
}

agree_pre_questions = tuple(item["id"] for item in pre_questions if item["answer_type"] == "agree-1-5")
agree_post_questions = tuple(item["id"] for item in post_questions if item["answer_type"] == "agree-1-5")
competency_labels = tuple(item["label"] for item in competencies)
pre_question_sections = tuple(item["title"] for item in pre_questions_data if item["title"] != "Competency")
post_question_sections = tuple(item["title"] for item in post_questions_data if item["title"] != "Competency")
all_question_sections = pre_question_sections + post_question_sections

survey_completion_map = {
    "pre": "pre",
    "working": "post",
    "awareness": "post",
    "practitioner": "post",
    "unknown": "post",
}
