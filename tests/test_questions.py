import itertools

from one_big_thing.learning.survey_handling import questions_data
from one_big_thing.learning.views import survey_questions_compulsory_field_map


def get_list_ids_for_page(page):
    return [question["id"] for question in page["questions"]]


def get_list_ids_for_section(section):
    ids_lists = [get_list_ids_for_page(page) for page in section]
    flat_list = [item for sublist in ids_lists for item in sublist]
    return flat_list


def get_list_all_question_ids_for_level(level):
    values = questions_data.values()
    sections = ["pre", "post", level]
    all_ids = [get_list_ids_for_section(section) for section in values if section in sections]
    flat_list = [item for sublist in all_ids for item in sublist]
    return flat_list


def test_question_ids_unique():
    competency_levels = ["awareness", "working", "practitioner", "unknown"]
    for level in competency_levels:
        ids_list = get_list_all_question_ids_for_level(level)
        unique_ids = set(ids_list)
        assert len(ids_list) == len(unique_ids), sorted(ids_list)


def test_mandatory_q_in_q_list():
    compulsory_dictionaries = list(survey_questions_compulsory_field_map.values())
    ids = [compulsory_dict.value() for compulsory_dict in compulsory_dictionaries]
    mandatory_set = set(itertools.chain.from_iterable(ids))
    working_level_ids = set(get_list_all_question_ids_for_level("working"))
    assert mandatory_set in working_level_ids, mandatory_set