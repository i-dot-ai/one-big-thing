from . import utils


class CourseType(utils.Choices):
    VIDEO = "Video"
    LINK = "Link"
    IN_PERSON = "In person"
    MULTIPLE = "Multiple"
    OTHER = "Other"


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
    OTHER = "Other"


class Profession(utils.Choices):
    ANALYSIS = "Analysis"
    COMMERCIAL = "Commercial"
    COMMUNICATIONS = "Communications"
    CORPORATE_FINANCE = "Corporate finance"
    COUNTER_FRAUD = "Counter fraud"
    DIGITAL_DATA_AND_TECHNOLOGY = "Digital, data and technology"
    ECONOMICS = "Economics"
    FINANCE = "Finance"
    FRAUD_ERROR_DEBTS_AND_GRANTS = "Fraud, error, debts and grants"
    HUMAN_RESOURCES = "Human resources"
    INTELLIGENCE_ANALYSIS = "Intelligence analysis"
    INTERNAL_AUDIT = "Internal audit"
    INTERNATIONAL_TRADE = "International trade"
    KNOWLEDGE_AND_INFORMATION_MANAGEMENT = "Knowledge and information management"
    LEGAL = "Legal"
    MEDICAL = "Medical"
    OCCUPATIONAL_PSYCHOLOGY = "Occupational psychology"
    OPERATIONAL_DELIVERY = "Operational delivery"
    OPERATIONAL_RESEARCH = "Operational research"
    PLANNING = "Planning"
    PLANNING_INSPECTION = "Planning inspection"
    POLICY = "Policy"
    PROJECT_DELIVERY = "Project delivery"
    PROPERTY = "Property"
    SCIENCE_AND_ENGINEERING = "Science and engineering"
    SECURITY = "Security"
    SOCIAL_RESEARCH = "Social research"
    STATISTICS = "Statistics"
    TAX = "Tax"
    VETERINARY = "Veterinary"
    OTHER = "Other"


class SurveyType(utils.Choices):
    PRE = "Pre"
    POST = "Post"
