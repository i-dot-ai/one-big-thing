from . import utils


class CourseType(utils.Choices):
    VIDEO = "Video"
    LINK = "Link"
    IN_PERSON = "In person"
    MULTIPLE = "Multiple"


class Grade(utils.Choices):
    ADMINISTRATIVE_ASSISTANT = "Administrative assistant"
    ADMINISTRATIVE_OFFICER = "Administrative officer"
    EXECUTIVE_OFFICER = "Executive officer"
    GRADE6 = "Grade 6"
    GRADE7 = "Grade 7"
    HIGHER_EXECUTIVE_OFFICER = "Higher executive officer"
    SCS_DEPUTY_DIRECTOR = "SCS: deputy director"
    SCS_DIRECTOR = "SCS: director"
    SCS_DIRECTOR_GENERAL = "SCS: director general"
    SCS_PERMANENT_SECRETARY = "SCS: permanent secretary"
    SENIOR_EXECUTIVE_OFFICER = "Senior executive officer"


class SurveyType(utils.Choices):
    PRE = "Pre"
    POST = "Post"
