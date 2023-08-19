from one_big_thing.learning.survey_handling import questions_data
from one_big_thing.learning.views import survey_questions_compulsory_field_map

def get_list_ids_for_page(page):
	return [question["id"] for question in page["questions"]]


def get_list_ids_for_section(section):
	ids_lists = [get_list_ids_for_page(page) for page in section]
	flat_list = [item for sublist in ids_lists for item in sublist]
	return flat_list


def get_list_all_question_ids():
	values = questions_data.values()
	all_ids = [get_list_ids_for_section(section) for section in values]
	flat_list = [item for sublist in all_ids for item in sublist]
	return flat_list


def test_question_ids_unique():
	ids_list = get_list_all_question_ids()
	unique_ids = set(ids_list)
	print(len(ids_list))
	print(len(unique_ids))
	assert len(ids_list) == len(unique_ids), ids_list.sort()

# def test_mandatory_q_in_list():
# 	mandatory_ids = 