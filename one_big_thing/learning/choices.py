from . import utils


class CourseType(utils.Choices):
    WRITTEN_RESOURCE = "Blog, article, book or other written resource"
    CIVIL_SERVICE_LIVE = "Civil Service Live event"
    CONVERSATION = "Conversation with colleagues"
    EVENT_CENTRAL = "Event - central"
    EVENT_DEPT = "Event - departmental"
    EVENT_EXTERNAL = "Event - external"
    FORMAL_TRAINING_CENTRAL = "Formal training - central"
    FORMAL_TRAINING_DEPT = "Formal training - departmental"
    FORMAL_TRAINING_EXTERNAL = "Formal training - external"
    INFORMAL_TRAINING = "Informal training (on-the-job training)"
    PODCAST_AUDIO = "Podcast or other audio"
    VIDEO = "Video or documentary"
    OTHER = "Other"


class Grade(utils.Choices):
    ADMINISTRATIVE_ASSISTANT = "Administrative assistant"
    ADMINISTRATIVE_OFFICER = "Administrative officer"
    EXECUTIVE_OFFICER = "Executive officer"
    HIGHER_EXECUTIVE_OFFICER = "Higher executive officer"
    SENIOR_EXECUTIVE_OFFICER = "Senior executive officer"
    GRADE7 = "Grade 7"
    GRADE6 = "Grade 6"
    SCS_DEPUTY_DIRECTOR = "SCS: Deputy director"
    SCS_DIRECTOR = "SCS: Director"
    SCS_DIRECTOR_GENERAL = "SCS: Director general"
    SCS_PERMANENT_SECRETARY = "SCS: Permanent secretary"
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


class YesNo(utils.Choices):
    yes = "Yes"
    no = "No"


class Satisfaction(utils.Choices):
    VERY_DISSATISFIED = "Very dissatisfied"
    DISSATISFIED = "Dissatisfied"
    NO_OPINION = "No opinion"
    SATISFIED = "Satisfied"
    VERY_SATISFIED = "Very satisfied"
