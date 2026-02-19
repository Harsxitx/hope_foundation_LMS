from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("LMS", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentRegistration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("batch_no", models.CharField(blank=True, max_length=100)),
                ("batch_timings", models.CharField(blank=True, max_length=100)),
                ("faculty_name", models.CharField(blank=True, max_length=150)),
                ("full_name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("unique_id_proof_type", models.CharField(blank=True, max_length=100)),
                ("unique_id_number", models.CharField(blank=True, max_length=100)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("contact_number", models.CharField(max_length=20)),
                ("whatsapp_number", models.CharField(blank=True, max_length=20)),
                ("gender", models.CharField(blank=True, max_length=30)),
                ("graduation_status", models.CharField(blank=True, max_length=100)),
                (
                    "current_education_qualification",
                    models.CharField(blank=True, max_length=150),
                ),
                ("ug_discipline", models.CharField(blank=True, max_length=150)),
                ("studied_college_in", models.CharField(blank=True, max_length=150)),
                ("applied_for_pg", models.CharField(blank=True, max_length=150)),
                (
                    "ug_pg_completion_timeline",
                    models.CharField(blank=True, max_length=200),
                ),
                (
                    "last_or_current_college_name",
                    models.CharField(blank=True, max_length=200),
                ),
                ("college_address", models.TextField(blank=True)),
                (
                    "currently_studying_or_working",
                    models.CharField(blank=True, max_length=100),
                ),
                ("work_office_designation_salary", models.TextField(blank=True)),
                ("internships_currently", models.CharField(blank=True, max_length=100)),
                (
                    "preparing_competitive_exams",
                    models.CharField(blank=True, max_length=100),
                ),
                ("course_help_in_competitive_exams", models.TextField(blank=True)),
                ("wants_job_immediately", models.CharField(blank=True, max_length=100)),
                ("plans_higher_education", models.TextField(blank=True)),
                ("preferred_job_location", models.CharField(blank=True, max_length=150)),
                ("comfortable_shift_jobs", models.CharField(blank=True, max_length=100)),
                ("can_spend_4_hours_daily", models.CharField(blank=True, max_length=100)),
                (
                    "can_submit_assignments_on_time",
                    models.CharField(blank=True, max_length=100),
                ),
                ("course_importance_and_need", models.TextField(blank=True)),
                ("can_attend_webinars", models.CharField(blank=True, max_length=100)),
                ("has_computer_or_laptop", models.CharField(blank=True, max_length=100)),
                ("has_smartphone", models.CharField(blank=True, max_length=100)),
                ("residential_address", models.TextField(blank=True)),
                ("pin_code", models.CharField(blank=True, max_length=20)),
                ("currently_staying_in", models.CharField(blank=True, max_length=150)),
                ("single_parent", models.CharField(blank=True, max_length=100)),
                ("parents_details", models.TextField(blank=True)),
                ("father_or_guardian_name", models.CharField(blank=True, max_length=200)),
                (
                    "father_or_guardian_contact",
                    models.CharField(blank=True, max_length=20),
                ),
                ("current_working_member", models.CharField(blank=True, max_length=150)),
                ("breadwinner_profession", models.CharField(blank=True, max_length=150)),
                ("annual_family_income", models.CharField(blank=True, max_length=100)),
                ("family_members_count", models.CharField(blank=True, max_length=50)),
                ("highest_family_education", models.CharField(blank=True, max_length=150)),
                ("social_category", models.CharField(blank=True, max_length=50)),
                ("application_status", models.CharField(blank=True, max_length=100)),
                ("referral_source", models.CharField(blank=True, max_length=200)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                ("account_created", models.BooleanField(default=False)),
                (
                    "created_user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="student_registration",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
