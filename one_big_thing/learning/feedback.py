feedback_questions_data = [
    {
        "id": "satisfaction",
        "text": "Overall, how do you feel about the service?",
        "answer_type": "radio",
    },
    {
        "id": "improve_the_service",
        "text": "How could we improve the service? (optional)",
        "extra_hint": "Do not include personal or financial information.",
        "answer_type": "textarea",
    },
    {
        "id": "take_part_in_user_research",
        "text": "Would you like to take part in user research to improve One Big Thing and the platform?",
        "answer_type": "radio",
    },
]

_yes_no = (
    ("yes", "Yes"),
    ("no", "No"),
)

answer_labels = {
    "satisfaction": {
        "VERY_DISSATISFIED": "Very dissatisfied",
        "DISSATISFIED": "Dissatisfied",
        "NO_OPINION": "No opinion",
        "SATISFIED": "Satisfied",
        "VERY_SATISFIED": "Very satisfied",
    },
    "take_part_in_user_research": dict(_yes_no),
}
