from one_big_thing.learning import choices, constants

pre_questions_data = [
    {
        "title": "How would you feel about making a decision based on information you're presented with? This might be numerical data like statistics or non-numerical data like user feedback.",  # noqa: E501
        "questions": [
            {
                "id": "confident-in-decisions",
                "text": "",
                "answer_type": "radio",
            },
        ],
    },
    {
        "title": "How would you feel about designing a graphic to communicate the results of a survey? This could be an infographic, chart or other visualisation.",  # noqa: E501
        "questions": [
            {
                "id": "confidence-graphic-survey",
                "text": "",
                "answer_type": "radio",
            },
        ],
    },
    {
        "title": "How would you feel about explaining to someone in your team what a chart of performance data is showing?",
        "questions": [
            {
                "id": "confidence-explaining-chart",
                "text": "",
                "answer_type": "radio",
            },
        ],
    },
    {
        "title": "To what extent do you agree or disagree with the following statement?",  # noqa: E501
        "questions": [
            {
                "id": "aware-of-the-aims",
                "text": "I am aware of the aims of One Big Thing",
                "answer_type": "agree-1-5",
            },
        ],
    },
    {
        "title": "To what extent do you agree or disagree with the following statements?",
        "questions": [
            {
                "id": "shared-identity",
                "text": "I feel connected with the wider Civil Service",
                "answer_type": "agree-1-5",
            },
            {
                "id": "identity-is-important",
                "text": "My identity as a civil servant is important to me",
                "answer_type": "agree-1-5",
            },
        ],
    },
    {
        "title": "To what extent do you agree or disagree with the following statements?",
        "questions": [
            {
                "id": "confident-day-to-day",
                "text": "I feel confident about using data in my day-to-day role",
                "answer_type": "agree-1-5",
            },
            {
                "id": "data-is-relevant-to-role",
                "text": "I think data is relevant to my role",
                "answer_type": "agree-1-5",
            },
            {
                "id": "use-data-effectively-day-to-day",
                "text": "I know how to use data effectively in my day-to-day role",
                "answer_type": "agree-1-5",
            },
            {
                "id": "data-support-day-to-day",
                "text": "I am aware of how data can support my day-to-day role",
                "answer_type": "agree-1-5",
            },
        ],
    },
    {
        "title": "Are you currently a line manager?",
        "questions": [
            {
                "id": "line-manager",
                "text": "",
                "answer_type": "radio",
            },
        ],
    },
    {
        "title": 'If you answered "yes" to the previous question, to what extent do you agree or disagree with the following statements?',  # noqa: E501
        "questions": [
            {
                "id": "help-team",
                "text": "I can help my team understand how data is relevant to their day-to-day roles",
                "answer_type": "radio",
            },
            {
                "id": "support-team",
                "text": "I know how to support my team to use data effectively in their day-to-day roles",
                "answer_type": "radio",
            },
            {
                "id": "coach-team",
                "text": "I know how to coach team members to make better use of data in their day to day roles",
                "answer_type": "radio",
            },
        ],
    },
    {
        "title": "In the last 6 months, have you done any type of training?",
        "questions": [
            {
                "id": "training-last-six-months",
                "text": "",
                "answer_type": "radio",
            },
        ],
    },
    {
        "title": 'If you answered "yes" to the previous question, did it have an analytical component (eg data, evaluation)',
        "questions": [
            {
                "id": "training-analytical-component",
                "text": "",
                "answer_type": "radio",
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
        "title": "Please rate how much you agree or disagree with the following statements:",
        "questions": [
            {
                "id": "shared-identity-post",
                "text": "Taking part in One Big Thing made me feel connected with other civil servants",
                "answer_type": "agree-1-5",
            },
            {
                "id": "identity-important-post",
                "text": "My identity as a Civil Servant is important to me",
                "answer_type": "agree-1-5",
            },
        ],
    },
    {
        "title": 'Following "One Big Thing",'
        "please rate how much you agree or disagree with each of the following statements:",
        "questions": [
            {
                "id": "confident-day-to-day",
                "text": "I feel confident about using data in my day-to-day role",
                "answer_type": "agree-1-5",
            },
            {
                "id": "data-is-relevant-to-role",
                "text": "I think data is relevant to my role",
                "answer_type": "agree-1-5",
            },
            {
                "id": "use-data-effectively-day-to-day",
                "text": "I know how to use data effectively in my day-to-day role",
                "answer_type": "agree-1-5",
            },
            {
                "id": "data-support-day-to-day",
                "text": "I am aware of how data can support my day-to-day role",
                "answer_type": "agree-1-5",
            },
        ],
    },
    {
        "title": "Are you currently a line manager?",
        "questions": [
            {
                "id": "line-manager-post",
                "text": "",
                "answer_type": "radio",
            },
        ],
    },
    {
        "title": 'If you answered "Yes" to the previous question please answer the following. To what extent do you agree or disagree with the following statements',
        "questions": [
            {
                "id": "help-team-post",
                "text": "I can help my team understand how data is relevant to their day-to-day roles",
                "answer_type": "radio",
            },
            {
                "id": "support-team-post",
                "text": "I know how to support my team to use data effectively in their day-to-day roles",
                "answer_type": "radio",
            },
            {
                "id": "coach-team-post",
                "text": "I know how to coach team members to make better use of data in their day to day roles",
                "answer_type": "radio",
            },
        ],
    },
]


shared_level_questions_data = [
    {
        "title": "Please rate how much you agree or disagree with the following statements",
        "questions": [
            {
                "id": "training-helped-learning",
                "text": "The online training helped my learning",
                "answer_type": "agree-1-5",
            },
            {
                "id": "conversations-helped-learning",
                "text": "Conversations with my team or line manager helped my learning",
                "answer_type": "agree-1-5",
            },
            {
                "id": "additional-resources-helped-learning",
                "text": "Additional learning resources helped my learning",
                "answer_type": "agree-1-5",
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
                "text": "The One Big Thing training was a good use of my time",
                "answer_type": "agree-1-5",
            },
            {
                "id": "improved-understanding-of-using-data",
                "text": "I have an improved understanding of how to use data in my day-to-day role",
                "answer_type": "agree-1-5",
            },
            {
                "id": "intend-to-participate-in-further-training",
                "text": "I intend to participate in further data training and initiatives",
                "answer_type": "agree-1-5",
            },
            {
                "id": "content-was-relevant-to-my-role",
                "text": "The content was relevant to my role",
                "answer_type": "agree-1-5",
            },
            {
                "id": "intend-to-apply-learning-in-my-role",
                "text": "I intend to apply learning from this training in my work",
                "answer_type": "agree-1-5",
            },
        ],
    },
    {
        "title": "Please rate how much you agree or disagree with the below statements",
        "questions": [
            {
                "id": "aware-of-aims",
                "text": "I am aware of the aims of One Big Thing",
                "answer_type": "agree-1-5",
            },
            {
                "id": "time-to-participate",
                "text": "I had sufficient time to participate in One Big Thing during the Autumn (September - December)",
                "answer_type": "agree-1-5",
            },
        ],
    },
    {
        "title": "Further questions",
        "questions": [
            {
                "id": "what-went-well",
                "text": "What if anything, went well about the training? Please use the space below to provide more details",  # noqa: E501
                "answer_type": "textarea",
                "max_length": 600,
            },
            {
                "id": "what-can-be-improved",
                "text": "Was there anything that could have been improved? Please use the space below to provide more details",  # noqa: E501
                "answer_type": "textarea",
                "max_length": 600,
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
                "id": "i-understand-what-data-means",
                "text": "I have a better understanding of what data means",
                "answer_type": "agree-1-5",
            },
            {
                "id": "better-at-interpreting-data",
                "text": "I am better at interpreting data",
                "answer_type": "agree-1-5",
            },
            {
                "id": "interested-in-working-with-data-in-day-to-day",
                "text": "I am more interested in working with data in my day-to-day role",
                "answer_type": "agree-1-5",
            },
            {
                "id": "more-confident-using-data-for-decisions",
                "text": "I feel more confident to use data to influence decisions",
                "answer_type": "agree-1-5",
            },
            {
                "id": "more-confident-communicating-data-to-influence-decisions",
                "text": "I can communicate data information more confidently to influence decisions",
                "answer_type": "agree-1-5",
            },
        ],
    },
    {
        "title": 'Following "One Big Thing", ' "please rate how much you agree or disagree with the below statements:",
        "questions": [
            {
                "id": "create-development-plan",
                "text": "I will create a development plan",
                "answer_type": "agree-1-5",
            },
            {
                "id": "add-learning-to-development-plan",
                "text": "I will add a new area of learning to my development plan",
                "answer_type": "agree-1-5",
            },
            {
                "id": "book-training",
                "text": "I will book a training course related to data",
                "answer_type": "agree-1-5",
            },
            {
                "id": "find-mentor",
                "text": "I will find a mentor",
                "answer_type": "agree-1-5",
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
                "id": "i-understand-different-data-techniques",
                "text": "I know more about how different data analysis techniques can be used to understand data",
                "answer_type": "agree-1-5",
            },
            {
                "id": "i-understand-critically-assessing-data",
                "text": "I understand better how to critically assess data collection, "
                "analysis and the insights derived from it",
                "answer_type": "agree-1-5",
            },
            {
                "id": "i-know-visualising-data",
                "text": "I know more about visualising and presenting data in a clear and concise way",
                "answer_type": "agree-1-5",
            },
            {
                "id": "importance-of-evaluating-outcomes-of-data-informed-decisions",
                "text": "I have learned about the importance of evaluating the outcomes of data-informed decisions",
                "answer_type": "agree-1-5",
            },
        ],
    },
    {
        "title": 'Following "One Big Thing", ' "please rate how much you agree or disagree with the below statements:",
        "questions": [
            {
                "id": "create-development-plan",
                "text": "I will create a development plan",
                "answer_type": "agree-1-5",
            },
            {
                "id": "add-learning-to-development-plan",
                "text": "I will add a new area of learning to my development plan",
                "answer_type": "agree-1-5",
            },
            {
                "id": "book-training",
                "text": "I will book a training course related to data",
                "answer_type": "agree-1-5",
            },
            {
                "id": "find-mentor",
                "text": "I will find a mentor",
                "answer_type": "agree-1-5",
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
                "insights more effectively to influence decisions",
                "answer_type": "agree-1-5",
            },
            {
                "id": "understand-how-to-quality-assure-data",
                "text": "I have a better understanding of how to quality assure data and analysis",
                "answer_type": "agree-1-5",
            },
            {
                "id": "anticipate-data-limitations",
                "text": "I understand better how to anticipate data limitations and uncertainty",
                "answer_type": "agree-1-5",
            },
            {
                "id": "understanding-ethics-for-data",
                "text": "I have a better understanding of data ethics",
                "answer_type": "agree-1-5",
            },
        ],
    },
    {
        "title": 'Following "One Big Thing", ' "please rate how much you agree or disagree with the below statements:",
        "questions": [
            {
                "id": "create-development-plan",
                "text": "I will create a development plan",
                "answer_type": "agree-1-5",
            },
            {
                "id": "add-learning-to-development-plan",
                "text": "I will add a new area of learning to my development plan",
                "answer_type": "agree-1-5",
            },
            {
                "id": "book-training",
                "text": "I will book a related training course",
                "answer_type": "agree-1-5",
            },
            {
                "id": "find-mentor",
                "text": "I will find a mentor/become a mentor",
                "answer_type": "agree-1-5",
            },
        ],
    },
    *shared_level_questions_data,
]

unknown_level_questions_data = [
    *shared_level_questions_data,
]

# _competencies = (
#     ("beginner", "Beginner"),
#     ("intermediate", "Intermediate"),
#     ("expert", "Expert"),
# )

_training_levels = (
    ("awareness", "Awareness"),
    ("working", "Working"),
    ("practitioner", "Practitioner"),
    ("unknown", "Don't know"),
)

_confidence_levels = (
    ("not-confident", "Not confident. I rarely do this"),
    (
        "confident",
        "Confident. I sometimes do this",
    ),
    (
        "very-confident",
        "Very confident. I often do this",
    ),
)

# _confident_in_decisions = (
#     ("not-confident", "Not confident"),
#     (
#         "confident",
#         "Confident",
#     ),
#     (
#         "very-confident",
#         "Very confident",
#     ),
# )

# _confident_explaining_graph = (
#     ("reluctant", "Reluctant"),
#     (
#         "willing-to-give-it-a-go",
#         "Willing to give it a go",
#     ),
#     (
#         "confident",
#         "Confident",
#     ),
# )

# _have_you_created_survey = (
#     ("no-i-couldnt-do-that", "No, I couldn't do that"),
#     (
#         "yes-i-could-do-that",
#         "Yes I could do that",
#     ),
#     (
#         "yes-i-could-teach-others",
#         "Yes, I could teach others how to do that",
#     ),
# )

# _have_you_believed_something_online = (
#     ("yes", "Yes"),
#     (
#         "no",
#         "No",
#     ),
#     (
#         "i-dont-think-so",
#         "I don't think so",
#     ),
# )

# _have_you_used_any_of_these = (
#     ("never-used", "Never used"),
#     (
#         "view",
#         "View",
#     ),
#     (
#         "create",
#         "Create",
#     ),
#     (
#         "automate",
#         "Automate",
#     ),
# )

_yes_no = (
    ("yes", "Yes"),
    ("no", "No"),
)

_yes_no_dont_know = (("yes", "Yes"), ("no", "No"), ("dont-know", "I don't know"))

questions_data = {
    "pre": pre_questions_data,
    "post": post_questions_data,
    "awareness": awareness_level_questions_data,
    "working": working_level_questions_data,
    "practitioner": practitioner_level_questions_data,
    "unknown": unknown_level_questions_data,
}

# competencies = tuple({"label": label, "name": name} for (label, name) in _competencies)
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
    "agree-1-5": {
        "1": "Strongly disagree",
        "2": "Disagree",
        "3": "Neither agree nor disagree",
        "4": "Agree",
        "5": "Strongly agree",
    },
    "likely-1-5": {
        "1": "Unlikely",
        "2": "Somewhat unlikely",
        "3": "Neither likely or unlikely",
        "4": "Somewhat likely",
        "5": "Likely",
    },
    "confident-in-decisions": dict(_confidence_levels),
    "confidence-graphic-survey": dict(_confidence_levels),
    "confidence-explaining-chart": dict(_confidence_levels),
    # "competency": dict(_competencies),
    "training-level": dict(_training_levels),
    "line-manager": dict(_yes_no),
    "help-team": dict(_yes_no_dont_know),
    "support-team": dict(_yes_no_dont_know),
    "coach-team": dict(_yes_no_dont_know),
    "line-manager-post": dict(_yes_no),
    "help-team-post": dict(_yes_no_dont_know),
    "support-team-post": dict(_yes_no_dont_know),
    "coach-team-post": dict(_yes_no_dont_know),
    "training-last-six-months": dict(_yes_no_dont_know),
    "training-analytical-component": dict(_yes_no_dont_know),
    "useful-learning-formats": choices.CourseType.mapping,
    "willing-to-follow-up": dict(_yes_no),
    # "confident-in-decisions": dict(_confident_in_decisions),
    # "confidence-explaining-graph": dict(_confident_explaining_graph),
    # "have-you-designed-a-survey": dict(_have_you_created_survey),
    # "believed-something-incorrect-online": dict(_have_you_believed_something_online),
    # "do-you-use-spreadsheets": dict(_have_you_used_any_of_these),
    # "do-you-use-dashboard-tools": dict(_have_you_used_any_of_these),
    # "do-you-use-coding-language": dict(_have_you_used_any_of_these),
}


agree_pre_questions = tuple(item["id"] for item in pre_questions if item["answer_type"] == "agree-1-5")
agree_post_questions = tuple(item["id"] for item in post_questions if item["answer_type"] == "agree-1-5")
# competency_labels = tuple(item["label"] for item in competencies)
# TODO: Is the "Competency" a thing? Has it gone, can it be removed?
# pre_question_sections = tuple(item["title"] for item in pre_questions_data if item["title"] != "Competency")
# post_question_sections = tuple(item["title"] for item in post_questions_data if item["title"] != "Competency")
pre_question_sections = tuple(item["title"] for item in pre_questions_data)
post_question_sections = tuple(item["title"] for item in post_questions_data)
all_question_sections = pre_question_sections + post_question_sections


survey_completion_map = {
    "pre": "pre",
    "working": "post",
    "awareness": "post",
    "practitioner": "post",
    "unknown": "post",
}
