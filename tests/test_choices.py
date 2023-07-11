from one_big_thing.learning import choices


def test_get_db_values():
    actual_values = choices.get_db_values(choices.CourseType.choices)
    expected_values = ["VIDEO", "LINK"]
    assert actual_values == expected_values, expected_values


def test_get_display_name():
    video = choices.get_display_name("VIDEO", choices.CourseType.options)
    other = choices.get_display_name("OTHER", choices.CourseType.options)
    assert video == "Video", video
    assert not other, other


def test_map_choice_or_other():
    video = choices.get_display_name("VIDEO", choices.CourseType.options)
    link = choices.get_display_name("LINK", choices.CourseType.options)
    assert video == "Video", video
    assert link == "Link", link


def test_turn_list_to_display_values():
    input_list = ["VIDEO", "LINK"]
    output_list = choices.turn_list_to_display_values(input_list, choices.CourseType.options)
    expected = ["Video", "Link"]
    assert output_list == expected, output_list


def test_restrict_choices():
    restricted_values = ["LINK"]
    actual = choices.restrict_choices(choices.CourseType.choices, restricted_values)
    expected = (("LINK", "Link"),)
    assert tuple(actual) == expected, tuple(actual)
