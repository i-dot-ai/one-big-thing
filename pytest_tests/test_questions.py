import itertools

from one_big_thing.learning.survey_handling import questions_data
from one_big_thing.learning.views import survey_questions_compulsory_field_map


def get_list_question_ids_for_section(section):
    # section eg "pre"
    section_list = questions_data[section]
    questions = [item["questions"] for item in section_list]
    questions = [item for sublist in questions for item in sublist]
    ids = [question["id"] for question in questions]
    return ids


def get_list_all_question_ids_for_level(level):
    sections = ["pre", "post", level]
    all_ids = [get_list_question_ids_for_section(section) for section in sections]
    flat_list = [item for sublist in all_ids for item in sublist]
    # May contain duplicates
    return flat_list


def test_question_ids_unique_for_section():
    sections = ["pre", "post", "awareness", "working", "practitioner", "unknown"]
    for section in sections:
        ids_list = get_list_question_ids_for_section(section)
        unique_ids = set(ids_list)
        assert len(ids_list) == len(unique_ids), sorted(ids_list)


def test_mandatory_q_in_q_list():
    compulsory_dictionaries = list(survey_questions_compulsory_field_map.values())
    ids = [v for compulsory_dict in compulsory_dictionaries for k, v in compulsory_dict.items()]
    mandatory_set = set(itertools.chain.from_iterable(ids))
    working_level_ids = set(get_list_all_question_ids_for_level("working"))
    assert mandatory_set.issubset(working_level_ids), mandatory_set
