from collections import OrderedDict

CABINET_OFFICE_LINK = "https://intranet.cabinetoffice.gov.uk/one-big-thing/"
HO_INTRANET_LINK = "https://ukhomeoffice.sharepoint.com/sites/prog3312/SitePages/One-Big-Thing.aspx"
HMRC_INTRANET_LINK = "https://hmrc.sharepoint.com/sites/COM142448518/SitePages/One-Big-Thing.aspx"
FCDO_INTRANET_LINK = "https://fcogovuk.sharepoint.com/sites/intranet-learning/SitePages/one-big-thing.aspx"
DEFRA_LINK = "https://defra.sharepoint.com/sites/Community739/SitePages/One-Big-Thing.aspx?OR=Teams-HL&CT=1693306749553"
ONS_LINK = "https://learninghub.ons.gov.uk/login/index.php"
HMRC_LINK = "https://hmrc.sharepoint.com/sites/COM142448518/SitePages/One-Big-Thing.aspx"
DFT_LINK = "https://intranet.dft.gov.uk/section/about-dft/one-big-thing-data-training-civil-servants"
OFSTED_LINK = "https://learnspace.ofsted.gov.uk/course/view.php?id=1205"
WELSH_GOVT_LINK = ""
DLUCH_LINK = "https://intranet.levellingup.gov.uk/intranet-login?redirect_to=%2Ftask%2Fone-big-thing-2023%2F"
DHSC_LINK = "https://intranet.dhsc.gov.uk/me-in-dh/my-learning-and-development-opportunities/one-big-thing/"
NCA_LINK = ""
DWP_LINK = (
    "https://intranet.dwp.gov.uk/section/working-dwp/dwp-learning-portal/essential-learning-and-induction/one-big-thing"
)
ORR_LINK = "https://intranet.orr.gov.uk/one-big-thing-2023"
CROWN_PROSECUTION_SERVICE_LINK = "https://cpsgovuk.sharepoint.com/hubs/hq/Operations/Pages/One-Big-Thing.aspx"
DEPARTMENT_FOR_ENERGY_SECURITY_AND_NET_ZERO_LINK = (
    "https://beisgov.sharepoint.com/sites/beisnews/SitePages/One-Big-Thing-%E2%80%93-DESNZ.aspx"
)
DEPARTMENT_FOR_SCIENCE_INFORMATION_AND_TECHNOLOGY_LINK = (
    "https://beisgov.sharepoint.com/sites/beisnews/SitePages/One-Big-Thing%20-%20DSIT.aspx"
)
DVLA_LINK = "https://dvla.sharepoint.com/sites/OrganisationTalentLearningOTL/SitePages/One-Big-Thing-2023.aspx"
HM_COURTS_AND_TRIBUNAL_SERVICE = "https://justiceuk.sharepoint.com/sites/HMCTSLandDHub/SitePages/Data.aspx"
MOD_LINK = (
    "https://modgovuk.sharepoint.com/sites/IntranetCivilianHRPeoplePortal/SitePages/MoD-Offer-(One-Big-Thing).aspx"
)
MOJ_LINK = "https://intranet.justice.gov.uk/guidance/hr/learning-and-development/capability-programmes/one-big-thing/"
DFE_LINK = "https://educationgovuk.sharepoint.com/sites/lvewp00394/SitePages/One-Big-Thing.aspx"
DCMS_LINK = "https://intranet.dcms.gov.uk/home/ls/community/my-ld-community"


# These are departments having the "streamlined view"
# Includes arms' length bodies that use main dept's intranet
# These keys are in a particular format to link to other lists
DEPARTMENTS_USING_INTRANET_LINKS = {
    "foreign-commonwealth-development-office": FCDO_INTRANET_LINK,
    "fcdo-services": FCDO_INTRANET_LINK,
    "hm-revenue-customs": HMRC_INTRANET_LINK,
    "home-office": HO_INTRANET_LINK,
    "hm-passport-office": HO_INTRANET_LINK,
    "immigration-enforcement": HO_INTRANET_LINK,
    "border-force": HO_INTRANET_LINK,
    "identity-and-passport-service": HO_INTRANET_LINK,
    "department-for-environment-food-rural-affairs": DEFRA_LINK,
    "forestry-commission": DEFRA_LINK,
    "the-water-services-regulation-authority": DEFRA_LINK,
    "animal-and-plant-health-agency": DEFRA_LINK,
    "centre-for-environment-fisheries-and-aquaculture-science": DEFRA_LINK,
    "rural-payments-agency": DEFRA_LINK,
    "veterinary-medicines-directorate": DEFRA_LINK,
    "agriculture-and-horticulture-development-board": DEFRA_LINK,
    "board-of-trustees-of-the-royal-botanic-gardens-kew": DEFRA_LINK,
    "consumer-council-for-water": DEFRA_LINK,
    "environment-agency": DEFRA_LINK,
    "joint-nature-conservation-committee": DEFRA_LINK,
    "marine-management-organisation": DEFRA_LINK,
    "natural-england": DEFRA_LINK,
    "office-for-environmental-protection": DEFRA_LINK,
    "seafish": DEFRA_LINK,
}

# These are departmental links for all departments we have them for,
# regardless of whether they are using the streamlined view
ALL_INTRANET_LINKS = OrderedDict(
    {
        "Cabinet Office": CABINET_OFFICE_LINK,
        "Crown Prosecution Service (CPS)": CROWN_PROSECUTION_SERVICE_LINK,
        "Department for Culture, Media and Sport (DCMS)": DCMS_LINK,
        "Department for Education (DfE)": DFE_LINK,
        "Department for Energy Security and Net Zero (DESNZ)": DEPARTMENT_FOR_ENERGY_SECURITY_AND_NET_ZERO_LINK,
        "Department for Environment, Food & Rural Affairs (Defra)": DEFRA_LINK,
        "Department of Health and Social Care (DHSC)": DHSC_LINK,
        "Department for Levelling Up, Housing and Communities (DLUHC)": DLUCH_LINK,
        "Department for Science, Innovation and Technology (DSIT)": DEPARTMENT_FOR_SCIENCE_INFORMATION_AND_TECHNOLOGY_LINK,  # noqa: E501
        "Department for Transport (DfT)": DFT_LINK,
        "Department for Work and Pensions (DWP)": DWP_LINK,
        "Driver and Vehicle Licensing Agency (DVLA)": DVLA_LINK,
        "Foreign, Commonwealth & Development Office (FCDO)": FCDO_INTRANET_LINK,
        "Home Office (HO)": HO_INTRANET_LINK,
        "HM Courts & Tribunal Service (HMCTS)": HM_COURTS_AND_TRIBUNAL_SERVICE,
        "HM Revenue & Customs (HMRC)": HMRC_INTRANET_LINK,
        "Ministry of Defence (MoD)": MOD_LINK,
        "Ministry of Justice (MoJ)": MOJ_LINK,
        "Office for National Statistics (ONS)": ONS_LINK,
        "Office of Rail and Road (ORR)": ORR_LINK,
        "Ofsted": OFSTED_LINK,
    }
)


INITIAL_COMPETENCY_DETERMINATION_QUESTIONS = [
    "confident-in-decisions",
    "confidence-graphic-survey",
    "confidence-explaining-chart",
]

AWARENESS = "awareness"
WORKING = "working"
PRACTITIONER = "practitioner"

COMPETENCY_DETERMINATION_MAPPING = {
    "not-confident": AWARENESS,
    "confident": WORKING,
    "very-confident": PRACTITIONER,
}

HOURS_LIMIT = 200
TOTAL_MINUTES_LIMIT = HOURS_LIMIT * 60 + 59
