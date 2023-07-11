from . import utils


class CourseType(utils.Choices):
    VIDEO = "Video"
    LINK = "Link"


def get_db_values(choices):
    output = [x[0] for x in choices]
    return output


def get_display_name(db_name, choices_options):
    result = [choice["text"] for choice in choices_options if choice["value"] == db_name]
    if not result:
        return None
    return result[0]


def map_choice_or_other(input, choices_options, append_separator=False):
    """
    If value is from the list of choices, return the display value.
    Otherwise this is the specified value for the 'other' choice,
    and return this.
    """
    if not input:
        mapped_value = ""
    mapped_value = get_display_name(input, choices_options)
    if not mapped_value:
        mapped_value = input
    if append_separator:
        mapped_value = f"{mapped_value}{utils.SEPARATOR}"
    return mapped_value


def turn_list_to_display_values(db_list, choices_options):
    if not db_list:
        return []
    output_list = [map_choice_or_other(x, choices_options) for x in db_list]
    return output_list


def map_other(pair, specified_other_description):
    if pair[0] == "OTHER":
        other_name = pair[1]
        full_other_name = f"{other_name} ({specified_other_description})"
        return ("OTHER", full_other_name)
    return pair


def restrict_choices(choices, values_to_restrict_to, specified_other=""):
    restricted = (choice for choice in choices if choice[0] in values_to_restrict_to)
    if specified_other and ("OTHER" in values_to_restrict_to):
        restricted = (map_other(x, specified_other) for x in restricted)
    return restricted
