import pytest
from django_test_migrations.migrator import Migrator

DEPARTMENTS = [
    "acas",
    "active-travel-england",
    "advisory-committee-on-releases-to-the-environment",
    "agriculture-and-horticulture-development-board",
    "animal-and-plant-health-agency",
    "attorney-generals-office",
    "board-of-trustees-of-the-royal-botanic-gardens-kew",
    "border-force",
    "british-wool",
    "broads-authority",
    "building-digital-uk",
    "cabinet-office",
    "central-civil-service-fast-stream",
    "centre-for-environment-fisheries-and-aquaculture-science",
    "charity-commission",
    "companies-house",
    "competition-and-markets-authority",
    "construction-industry-training-board",
    "consumer-council-for-water",
    "covent-garden-market-authority",
    "criminal-injuries-compensation-appeals-panel",
    "crown-commercial-service",
    "crown-prosecution-service",
    "dartmoor-national-park-authority",
    "defence-electronics-and-components-agency",
    "defence-equipment-and-support",
    "defence-nuclear-organisation",
    "defence-science-and-technology-laboratory",
    "science-advisory-council",
    "department-for-business-and-trade",
    "department-for-culture-media-and-sport",
    "department-for-education",
    "department-for-energy-security-and-net-zero",
    "department-for-environment-food-rural-affairs",
    "department-for-levelling-up-housing-and-communities",
    "department-for-science-innovation-and-technology",
    "department-for-transport",
    "department-of-health-and-social-care",
    "disclosure-and-barring-service",
    "driver-and-vehicle-licensing-agency",
    "driver-and-vehicle-standards-agency",
    "dwp-central-analysis-and-science",
    "dwp-change-group",
    "dwp-communications",
    "dwp-corporate-transformantion",
    "dwp-digital-it",
    "dwp-finance-group",
    "dwp-ops-cmg",
    "dwp-ops-cfed",
    "dwp-ops-ce",
    "dwp-ops-drs",
    "dwp-ops-rs",
    "dwp-ops-sm",
    "dwp-ops-spd",
    "dwp-ops-dsdmwa",
    "dwp-ops-uco",
    "dwp-people-and-capability",
    "dwp-policy-team",
    "dwp-private-office",
    "dwp-strategy-directorate",
    "dwp-other",
    "education-and-skills-funding-agency",
    "engineering-construction-industry-training-board",
    "environment-agency",
    "the-equality-hub",
    "estyn",
    "exmoor-national-park-authority",
    "fcdo-services",
    "flood-re",
    "food-standards-agency",
    "foreign-commonwealth-development-office",
    "forestry-commission",
    "government-actuarys-department",
    "government-commercial-organisation",
    "government-equalities-office",
    "government-internal-audit-agency",
    "government-legal-department",
    "government-property-agency",
    "health-and-safety-executive",
    "hm-courts-and-tribunals-service",
    "hm-inspectorate-of-prisons",
    "hm-inspectorate-of-probation",
    "land-registry",
    "hm-prison-and-probation-service",
    "hm-revenue-customs",
    "hm-treasury",
    "home-office",
    "hm-passport-office",
    "identity-and-passport-service",
    "immigration-enforcement",
    "independent-agricultural-appeals-panel",
    "independent-monitoring-boards-of-prisons-immigration-removal-centres-and-short-term-holding-rooms",
    "infrastructure-and-projects-authority",
    "institute-for-apprenticeships-and-technical-education",
    "intellectual-property-office",
    "joint-nature-conservation-committee",
    "judicial-appointments-and-conduct-ombudsman",
    "judicial-office",
    "lake-district-national-park-authority",
    "law-commission",
    "legal-aid-agency",
    "located",
    "marine-management-organisation",
    "maritime-and-coastguard-agency",
    "medicines-and-healthcare-products-regulatory-agency",
    "met-office",
    "ministry-of-defence-civilian",
    "ministry-of-defence-military",
    "ministry-of-justice",
    "single-financial-guidance-body",
    "national-crime-agency",
    "national-forest-company",
    "national-infrastructure-commission",
    "natural-england",
    "new-forest-national-park-authority",
    "north-york-moors-national-park",
    "northern-ireland-executive",
    "northern-ireland-office",
    "northumberland-national-park-authority",
    "ns-i",
    "oak-national-academy",
    "office-for-environmental-protection",
    "office-for-national-statistics",
    "ofsted",
    "office-for-students",
    "ofgem",
    "ofqual",
    "office-of-rail-and-road",
    "office-of-the-advocate-general-for-scotland",
    "office-of-the-children-s-commissioner",
    "the-office-of-the-leader-of-the-house-of-commons",
    "office-of-the-leader-of-the-house-of-lords",
    "office-of-the-public-guardian",
    "office-of-the-secretary-of-state-for-scotland",
    "office-of-the-secretary-of-state-for-wales",
    "official-solicitor-and-public-trustee",
    "peak-district-national-park",
    "planning-inspectorate",
    "plant-varieties-and-seeds-tribunal",
    "prime-ministers-office-10-downing-street",
    "prisons-and-probation-ombudsman",
    "queen-elizabeth-ii-conference-centre",
    "royal-fleet-auxiliary",
    "rural-payments-agency",
    "the-scottish-government",
    "seafish",
    "the-sentencing-council-for-england-and-wales",
    "serious-fraud-office",
    "social-work-england",
    "south-downs-national-park-authority",
    "standards-and-testing-agency",
    "student-loans-company",
    "submarine-delivery-agency",
    "supreme-court-of-the-united-kingdom",
    "teaching-regulation-agency",
    "insolvency-service",
    "the-national-archives",
    "the-water-services-regulation-authority",
    "uk-debt-management-office",
    "uk-export-finance",
    "uk-health-security-agency",
    "uk-hydrographic-office",
    "uk-space-agency",
    "uk-statistics-authority",
    "valuation-office-agency",
    "vehicle-certification-agency",
    "veterinary-medicines-directorate",
    "veterinary-products-committee",
    "victims-commissioner",
    "welsh-government",
    "welsh-revenue-authority",
    "wilton-park",
    "yorkshire-dales-national-park-authority",
    "other",
    "other-civil-servant",
    "other-public-servant",
    None,
]


@pytest.mark.django_db
def test_0020_department():
    migrator = Migrator(database="default")

    old_state = migrator.apply_initial_migration(("learning", "0019_auto_20231025_1255"))
    OldUser = old_state.apps.get_model("learning", "User")  # noqa: N806

    for department in DEPARTMENTS:
        OldUser.objects.create(email=f"someone@{department}.gov.uk", department=department, password="p4ssw0rd!")

    new_state = migrator.apply_tested_migration(
        ("learning", "0020_department"),
    )
    NewUser = new_state.apps.get_model("learning", "User")  # noqa: N806

    for department in DEPARTMENTS:
        new_user = NewUser.objects.get(department__code=department)
        if department is None:
            assert new_user.old_department is None
            assert new_user.old_department is None
        else:
            assert new_user.old_department == new_user.department.code

    # Cleanup:
    migrator.reset()
