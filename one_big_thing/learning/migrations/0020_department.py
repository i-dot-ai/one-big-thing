# Generated by Django 3.2.22 on 2023-10-20 10:48
import json
import os

import django
from django.db import migrations, models

with open(os.path.join(os.path.abspath("."), "departments.csv")) as f:
    rows = [json.loads(f"[{row}]") for row in f.readlines()]
    DEPARTMENTS = rows[1:]


def populate_department_model(apps, schema_editor):
    Department = apps.get_model("learning", "Department")

    for code, display, parent, url in DEPARTMENTS:
        Department.objects.create(code=code, display=display, parent=parent, url=url)


def populate_user_model_with_departments(apps, schema_editor):
    User = apps.get_model("learning", "User")
    Department = apps.get_model("learning", "Department")

    for user in User.objects.all():
        user.new_department = Department.objects.get(code=user.department)
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0019_choices"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(help_text="unique code for department", max_length=128, unique=True)),
                ("display", models.CharField(help_text="display name", max_length=128)),
                (
                    "parent",
                    models.CharField(
                        choices=[
                            ("ATTORNEY_GENERALS_DEPARTMENTS", "Attorney General's Departments"),
                            ("CABINET_OFFICE", "Cabinet Office"),
                            ("CHANCELLORS_OTHER_DEPARTMENTS", "Chancellor's other departments"),
                            ("CHARITY_COMMISSION", "Charity Commission"),
                            ("COMPETITION_AND_MARKETS_AUTHORITY", "Competition and Markets Authority"),
                            ("CROWN_PROSECUTION_SERVICE", "Crown Prosecution Service"),
                            ("DEPARTMENT_FOR_BUSINESS_AND_TRADE", "Department for Business and Trade "),
                            ("DEPARTMENT_FOR_CULTURE_MEDIA_AND_SPORT", "Department for Culture, Media & Sport"),
                            ("DEPARTMENT_FOR_EDUCATION", "Department for Education"),
                            (
                                "DEPARTMENT_FOR_ENERGY_SECURITY_AND_NET_ZERO",
                                "Department for Energy Security & Net Zero",
                            ),
                            (
                                "DEPARTMENT_FOR_ENVIRONMENT_FOOD_AND_RURAL_AFFAIRS",
                                "Department for Environment Food & Rural Affairs",
                            ),
                            (
                                "DEPARTMENT_FOR_LEVELLING_UP_HOUSING_AND_COMMUNITIES",
                                "Department for Levelling Up, Housing and Communities",
                            ),
                            (
                                "DEPARTMENT_FOR_SCIENCE_INNOVATION_AND_TECHNOLOGY",
                                "Department for Science, Innovation & Technology",
                            ),
                            ("DEPARTMENT_FOR_TRANSPORT", "Department for Transport"),
                            ("DEPARTMENT_FOR_WORK_AND_PENSIONS", "Department for Work & Pensions"),
                            ("DEPARTMENT_OF_HEALTH_AND_SOCIAL_CARE", "Department of Health & Social Care"),
                            ("FOOD_STANDARDS_AGENCY", "Food Standards Agency"),
                            (
                                "FOREIGN_COMMONWEALTH_AND_DEVELOPMENT_OFFICE",
                                "Foreign, Commonwealth & Development Office",
                            ),
                            ("HM_LAND_REGISTRY", "HM Land Registry"),
                            ("HM_REVENUE_AND_CUSTOMS", "HM Revenue & Customs"),
                            ("HM_TREASURY", "HM Treasury"),
                            ("HOME_OFFICE", "Home Office"),
                            ("MINISTRY_OF_DEFENCE", "Ministry of Defence"),
                            ("MINISTRY_OF_JUSTICE", "Ministry of Justice"),
                            ("NATIONAL_CRIME_AGENCY", "National Crime Agency"),
                            ("NORTHERN_IRELAND_EXECUTIVE", "Northern Ireland Executive"),
                            ("NORTHERN_IRELAND_OFFICE", "Northern Ireland Office"),
                            (
                                "OFFICE_OF_THE_SECRETARY_OF_STATE_FOR_WALES",
                                "Office of the Secretary of State for Wales",
                            ),
                            (
                                "OFFICE_OF_THE_SECRETARY_OF_STATE_FOR_SCOTLAND",
                                "Office of the Secretary of State for Scotland",
                            ),
                            ("OFGEM", "Ofgem"),
                            ("OFQUAL", "Ofqual"),
                            ("OTHER", "Other"),
                            ("OFSTED", "Ofsted"),
                            ("OFFICE_OF_RAIL_AND_ROAD", "Office of Rail and Road"),
                            ("SCOTTISH_GOVERNMENT", "Scottish Government"),
                            ("SUPREME_COURT_OF_THE_UNITED_KINGDOM", "Supreme Court of the United Kingdom"),
                            ("THE_NATIONAL_ARCHIVES", "The National Archives"),
                            ("UK_EXPORT_FINANCE", "UK Export Finance"),
                            ("UK_STATISTICS_AUTHORITY", "UK Statistics Authority"),
                            ("WATER_SERVICES_REGULATION_AUTHORITY", "Water Services Regulation Authority"),
                            ("WELSH_GOVERNMENT", "Welsh Government"),
                        ],
                        help_text="parent department",
                        max_length=128,
                    ),
                ),
                ("url", models.URLField(blank=True, help_text="intranet link", null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RunPython(populate_department_model),
        migrations.AddField(
            model_name="user",
            name="new_department",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="learning.department"
            ),
        ),
        migrations.RunPython(populate_user_model_with_departments),
        migrations.RemoveIndex(
            model_name="user",
            name="learning_us_departm_081e46_idx",
        ),
        migrations.AlterField(
            model_name="user",
            name="department",
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.RenameField(
            model_name="user",
            old_name="department",
            new_name="old_department",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="new_department",
            new_name="department",
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["department", "grade", "profession", "has_completed_pre_survey", "has_completed_post_survey"],
                name="learning_us_departm_a9c393_idx",
            ),
        ),
    ]
