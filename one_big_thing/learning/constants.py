from collections import OrderedDict

HO_INTRANET_LINK = "https://ukhomeoffice.sharepoint.com/sites/prog3312/SitePages/One-Big-Thing.aspx"
HMRC_INTRANET_LINK = "http://www.example.com"
FCDO_INTRANET_LINK = "https://fcogovuk.sharepoint.com/sites/intranet-learning/SitePages/one-big-thing.aspx"
DEFRA_LINK = ""
ONS_LINK = "https://learninghub.ons.gov.uk/login/index.php"
HMRC_LINK = ""
DFT_LINK = ""
OFSTED_LINK = "https://learnspace.ofsted.gov.uk/course/view.php?id=1205"
WELSH_GOVT_LINK = ""
DLUCH_LINK = ""
DHSC_LINK = ""
NCA_LINK = ""
DWP_LINK = (
    "https://intranet.dwp.gov.uk/section/working-dwp/dwp-learning-portal/essential-learning-and-induction/one-big-thing"
)
ORR_LINK = "https://intranet.orr.gov.uk/one-big-thing-2023"


# TODO - what are the arms' length bodies that will also use these?
# TODO - get all links
# These are departments having the "streamlined view"
# These keys are in a particular format to link to other lists
DEPARTMENTS_USING_INTRANET_LINKS = {
    "foreign-commonweath-development-office": FCDO_INTRANET_LINK,
    "hm-revenue-customs": HMRC_INTRANET_LINK,
    "home-office": HO_INTRANET_LINK,
}

# These are departmental links for all departments we have them for,
# regardless of whether they are using the streamlined view
ALL_INTRANET_LINKS = OrderedDict({
    "Department for Environment, Food and Rural Affairs (Defra)": DEFRA_LINK,
    "Department for Levelling Up, Housing and Communities (DLUHC)": DLUCH_LINK,
    "Department for Transport (DfT)": DFT_LINK,
    "Department for Work and Pensions": DWP_LINK,
    "Department of Health and Social Care (DHSC)": DHSC_LINK,
    "Foreign, Commonwealth & Development Office (FCDO)": FCDO_INTRANET_LINK,
    "HM Revenue and Customs (HMRC)": HMRC_INTRANET_LINK,
    "Home Office": HO_INTRANET_LINK,
    "National Crime Agency (NCA)": NCA_LINK,
    "Office for National Statistics (ONS)": ONS_LINK,
    "Office of Rail and Road (ORR)": ORR_LINK,
    "Ofsted": OFSTED_LINK,
    "Welsh Government": WELSH_GOVT_LINK,
})
