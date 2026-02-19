from django.contrib.auth.models import User
from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    course_name = models.CharField(max_length=200, blank=True)
    course_duration = models.CharField(max_length=100, blank=True)
    progress_percent = models.PositiveIntegerField(default=0)
    enrolled_on = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.user.id})"


class StudentRegistration(models.Model):
    # 1. Basic Information
    batch_no = models.CharField(max_length=100, blank=True)
    batch_timings = models.CharField(max_length=100, blank=True)
    faculty_name = models.CharField(max_length=150, blank=True)

    # 2. Personal Details
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    unique_id_proof_type = models.CharField(max_length=100, blank=True)
    unique_id_number = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=30, blank=True)

    # 3. Educational Details
    graduation_status = models.CharField(max_length=100, blank=True)
    current_education_qualification = models.CharField(max_length=150, blank=True)
    ug_discipline = models.CharField(max_length=150, blank=True)
    studied_college_in = models.CharField(max_length=150, blank=True)
    applied_for_pg = models.CharField(max_length=150, blank=True)
    ug_pg_completion_timeline = models.CharField(max_length=200, blank=True)
    last_or_current_college_name = models.CharField(max_length=200, blank=True)
    college_address = models.TextField(blank=True)

    # 4. Current Status (Study / Work)
    currently_studying_or_working = models.CharField(max_length=100, blank=True)
    work_office_designation_salary = models.TextField(blank=True)
    internships_currently = models.CharField(max_length=100, blank=True)
    preparing_competitive_exams = models.CharField(max_length=100, blank=True)
    course_help_in_competitive_exams = models.TextField(blank=True)

    # 5. Career Plans & Preferences
    wants_job_immediately = models.CharField(max_length=100, blank=True)
    plans_higher_education = models.TextField(blank=True)
    preferred_job_location = models.CharField(max_length=150, blank=True)
    comfortable_shift_jobs = models.CharField(max_length=100, blank=True)

    # 6. Course Commitment & Availability
    can_spend_4_hours_daily = models.CharField(max_length=100, blank=True)
    can_submit_assignments_on_time = models.CharField(max_length=100, blank=True)
    course_importance_and_need = models.TextField(blank=True)
    can_attend_webinars = models.CharField(max_length=100, blank=True)

    # 7. Technical Readiness
    has_computer_or_laptop = models.CharField(max_length=100, blank=True)
    has_smartphone = models.CharField(max_length=100, blank=True)

    # 8. Residential Details
    residential_address = models.TextField(blank=True)
    pin_code = models.CharField(max_length=20, blank=True)
    currently_staying_in = models.CharField(max_length=150, blank=True)

    # 9. Family Details
    single_parent = models.CharField(max_length=100, blank=True)
    parents_details = models.TextField(blank=True)
    father_or_guardian_name = models.CharField(max_length=200, blank=True)
    father_or_guardian_contact = models.CharField(max_length=20, blank=True)
    current_working_member = models.CharField(max_length=150, blank=True)
    breadwinner_profession = models.CharField(max_length=150, blank=True)
    annual_family_income = models.CharField(max_length=100, blank=True)
    family_members_count = models.CharField(max_length=50, blank=True)
    highest_family_education = models.CharField(max_length=150, blank=True)
    social_category = models.CharField(max_length=50, blank=True)

    # 10. Course Application Status
    application_status = models.CharField(max_length=100, blank=True)
    referral_source = models.CharField(max_length=200, blank=True)

    # Admin handling
    submitted_at = models.DateTimeField(auto_now_add=True)
    account_created = models.BooleanField(default=False)
    created_user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_registration",
    )

    def __str__(self):
        return f"{self.full_name} ({self.email})"
