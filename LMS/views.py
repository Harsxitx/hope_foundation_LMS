import csv

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date

from .models import StudentProfile, StudentRegistration


REGISTRATION_SECTIONS = [
    (
        "1. Basic Information",
        [
            ("batch_no", "Batch No", "text"),
            ("batch_timings", "Batch Timings", "text"),
            ("faculty_name", "Faculty Name", "text"),
        ],
    ),
    (
        "2. Personal Details",
        [
            ("full_name", "Full Name (As per your certificate)", "text"),
            ("email", "Email ID", "email"),
            ("unique_id_proof_type", "Type of Unique ID Proof", "text"),
            ("unique_id_number", "Unique ID Number", "text"),
            ("date_of_birth", "Date Of Birth", "date"),
            ("contact_number", "Contact Number", "text"),
            ("whatsapp_number", "WhatsApp Number", "text"),
            ("gender", "Gender", "text"),
        ],
    ),
    (
        "3. Educational Details",
        [
            ("graduation_status", "Graduation Status", "text"),
            ("current_education_qualification", "Current Education Qualification", "text"),
            ("ug_discipline", "UG Discipline", "text"),
            ("studied_college_in", "Studied / Studying College in?", "text"),
            ("applied_for_pg", "If completed UG, have you applied for PG?", "text"),
            (
                "ug_pg_completion_timeline",
                "If Final Year student (UG/PG), when will course be completed?",
                "text",
            ),
            ("last_or_current_college_name", "Last / Current College Name", "text"),
            ("college_address", "College Address", "textarea"),
        ],
    ),
    (
        "4. Current Status (Study / Work)",
        [
            ("currently_studying_or_working", "Currently Studying or Working?", "text"),
            (
                "work_office_designation_salary",
                "If Working - Office Name, Designation, Salary",
                "textarea",
            ),
            ("internships_currently", "Do you have any internships going on currently?", "text"),
            ("preparing_competitive_exams", "Are you preparing for any Competitive Exams?", "text"),
            (
                "course_help_in_competitive_exams",
                "If yes, how will this course help in competitive exams?",
                "textarea",
            ),
        ],
    ),
    (
        "5. Career Plans & Preferences",
        [
            (
                "wants_job_immediately",
                "Interested in getting a job immediately after finishing course?",
                "text",
            ),
            ("plans_higher_education", "Planning for higher education? If yes, details", "textarea"),
            ("preferred_job_location", "Preferred Job Location", "text"),
            ("comfortable_shift_jobs", "Comfortable with shift timing jobs?", "text"),
        ],
    ),
    (
        "6. Course Commitment & Availability",
        [
            (
                "can_spend_4_hours_daily",
                "Can you spend 4 hours daily for Cloud Computing Classes?",
                "text",
            ),
            (
                "can_submit_assignments_on_time",
                "Can you submit Assignments/Projects on time?",
                "text",
            ),
            (
                "course_importance_and_need",
                "How important is this course to you? Why do you need it?",
                "textarea",
            ),
            ("can_attend_webinars", "Can you attend webinars apart from class timings?", "text"),
        ],
    ),
    (
        "7. Technical Readiness",
        [
            ("has_computer_or_laptop", "Do you have a Computer/Laptop?", "text"),
            ("has_smartphone", "Do you have a Smartphone?", "text"),
        ],
    ),
    (
        "8. Residential Details",
        [
            ("residential_address", "Complete Residential Address", "textarea"),
            ("pin_code", "Pin Code", "text"),
            ("currently_staying_in", "Currently Staying In", "text"),
        ],
    ),
    (
        "9. Family Details",
        [
            ("single_parent", "Single Parent?", "text"),
            ("parents_details", "Parent/s Details", "textarea"),
            ("father_or_guardian_name", "Name of Father / Guardian", "text"),
            ("father_or_guardian_contact", "Contact Number of Father / Guardian", "text"),
            ("current_working_member", "Who is currently working?", "text"),
            ("breadwinner_profession", "Profession of Breadwinner in Family", "text"),
            ("annual_family_income", "Annual Family Income", "text"),
            ("family_members_count", "Number of Family Members (excluding parents)", "text"),
            ("highest_family_education", "Highest Education Qualification in Family", "text"),
            ("social_category", "Category (Gen/OBC/SC/ST)", "text"),
        ],
    ),
    (
        "10. Course Application Status",
        [
            ("application_status", "Applying for FIRST TIME or REJOINING?", "text"),
            ("referral_source", "How did you come to know about this course?", "text"),
        ],
    ),
]

SELECT_OPTIONS = {
    "unique_id_proof_type": [
        "Aadhaar",
        "PAN",
        "Passport",
        "Voter ID",
        "Driving License",
        "Other",
    ],
    "gender": ["Male", "Female", "Other", "Prefer not to say"],
    "graduation_status": ["Completed", "Final Year", "Pursuing", "Not Started"],
    "currently_studying_or_working": ["Studying", "Working", "Both", "Neither"],
    "internships_currently": ["Yes", "No"],
    "preparing_competitive_exams": ["Yes", "No"],
    "wants_job_immediately": ["Yes", "No"],
    "comfortable_shift_jobs": ["Yes", "No"],
    "can_spend_4_hours_daily": ["Yes", "No"],
    "can_submit_assignments_on_time": ["Yes", "No"],
    "can_attend_webinars": ["Yes", "No"],
    "has_computer_or_laptop": ["Yes", "No"],
    "has_smartphone": ["Yes", "No"],
    "single_parent": ["Yes", "No"],
    "social_category": ["Gen", "OBC", "SC", "ST", "Other"],
    "application_status": ["FIRST TIME", "REJOINING"],
}

REQUIRED_FIELDS = {"full_name", "email", "contact_number"}


def registration_form_sections():
    sections = []
    for section_title, fields in REGISTRATION_SECTIONS:
        formatted_fields = []
        for field_name, field_label, field_type in fields:
            options = SELECT_OPTIONS.get(field_name, [])
            formatted_fields.append(
                {
                    "name": field_name,
                    "label": field_label,
                    "type": "select" if options else field_type,
                    "options": options,
                    "required": field_name in REQUIRED_FIELDS,
                }
            )
        sections.append((section_title, formatted_fields))
    return sections


def filtered_registrations(request):
    q = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "all").strip()
    batch_filter = request.GET.get("batch", "").strip()

    registrations = StudentRegistration.objects.select_related("created_user").order_by(
        "-submitted_at"
    )

    if q:
        registrations = registrations.filter(
            Q(full_name__icontains=q)
            | Q(email__icontains=q)
            | Q(contact_number__icontains=q)
            | Q(referral_source__icontains=q)
        )

    if status_filter == "pending":
        registrations = registrations.filter(account_created=False)
    elif status_filter == "created":
        registrations = registrations.filter(account_created=True)

    if batch_filter:
        registrations = registrations.filter(batch_no__icontains=batch_filter)

    return registrations, q, status_filter, batch_filter


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin_dashboard")
        return redirect("student_dashboard")
    return render(request, "home.html")


def student_register_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        contact_number = request.POST.get("contact_number", "").strip()

        if not full_name or not email or not contact_number:
            messages.error(
                request,
                "Full Name, Email ID, and Contact Number are required.",
            )
            return redirect("student_register")

        student_registration = StudentRegistration(
            batch_no=request.POST.get("batch_no", "").strip(),
            batch_timings=request.POST.get("batch_timings", "").strip(),
            faculty_name=request.POST.get("faculty_name", "").strip(),
            full_name=full_name,
            email=email,
            unique_id_proof_type=request.POST.get("unique_id_proof_type", "").strip(),
            unique_id_number=request.POST.get("unique_id_number", "").strip(),
            date_of_birth=parse_date(request.POST.get("date_of_birth", "").strip() or ""),
            contact_number=contact_number,
            whatsapp_number=request.POST.get("whatsapp_number", "").strip(),
            gender=request.POST.get("gender", "").strip(),
            graduation_status=request.POST.get("graduation_status", "").strip(),
            current_education_qualification=request.POST.get(
                "current_education_qualification", ""
            ).strip(),
            ug_discipline=request.POST.get("ug_discipline", "").strip(),
            studied_college_in=request.POST.get("studied_college_in", "").strip(),
            applied_for_pg=request.POST.get("applied_for_pg", "").strip(),
            ug_pg_completion_timeline=request.POST.get(
                "ug_pg_completion_timeline", ""
            ).strip(),
            last_or_current_college_name=request.POST.get(
                "last_or_current_college_name", ""
            ).strip(),
            college_address=request.POST.get("college_address", "").strip(),
            currently_studying_or_working=request.POST.get(
                "currently_studying_or_working", ""
            ).strip(),
            work_office_designation_salary=request.POST.get(
                "work_office_designation_salary", ""
            ).strip(),
            internships_currently=request.POST.get("internships_currently", "").strip(),
            preparing_competitive_exams=request.POST.get(
                "preparing_competitive_exams", ""
            ).strip(),
            course_help_in_competitive_exams=request.POST.get(
                "course_help_in_competitive_exams", ""
            ).strip(),
            wants_job_immediately=request.POST.get("wants_job_immediately", "").strip(),
            plans_higher_education=request.POST.get("plans_higher_education", "").strip(),
            preferred_job_location=request.POST.get("preferred_job_location", "").strip(),
            comfortable_shift_jobs=request.POST.get("comfortable_shift_jobs", "").strip(),
            can_spend_4_hours_daily=request.POST.get(
                "can_spend_4_hours_daily", ""
            ).strip(),
            can_submit_assignments_on_time=request.POST.get(
                "can_submit_assignments_on_time", ""
            ).strip(),
            course_importance_and_need=request.POST.get(
                "course_importance_and_need", ""
            ).strip(),
            can_attend_webinars=request.POST.get("can_attend_webinars", "").strip(),
            has_computer_or_laptop=request.POST.get("has_computer_or_laptop", "").strip(),
            has_smartphone=request.POST.get("has_smartphone", "").strip(),
            residential_address=request.POST.get("residential_address", "").strip(),
            pin_code=request.POST.get("pin_code", "").strip(),
            currently_staying_in=request.POST.get("currently_staying_in", "").strip(),
            single_parent=request.POST.get("single_parent", "").strip(),
            parents_details=request.POST.get("parents_details", "").strip(),
            father_or_guardian_name=request.POST.get(
                "father_or_guardian_name", ""
            ).strip(),
            father_or_guardian_contact=request.POST.get(
                "father_or_guardian_contact", ""
            ).strip(),
            current_working_member=request.POST.get("current_working_member", "").strip(),
            breadwinner_profession=request.POST.get("breadwinner_profession", "").strip(),
            annual_family_income=request.POST.get("annual_family_income", "").strip(),
            family_members_count=request.POST.get("family_members_count", "").strip(),
            highest_family_education=request.POST.get(
                "highest_family_education", ""
            ).strip(),
            social_category=request.POST.get("social_category", "").strip(),
            application_status=request.POST.get("application_status", "").strip(),
            referral_source=request.POST.get("referral_source", "").strip(),
        )
        student_registration.save()
        messages.success(
            request,
            "Registration submitted successfully. Admin will create your User ID and Password.",
        )
        return redirect("home")

    return render(
        request,
        "student_register.html",
        {"sections": registration_form_sections()},
    )


def student_login_view(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect("student_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_staff:
            login(request, user)
            return redirect("student_dashboard")

        messages.error(request, "Invalid student credentials.")

    return render(request, "student_login.html")


def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")

        messages.error(request, "Invalid admin credentials.")

    return render(request, "admin_login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def student_dashboard(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")

    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    return render(request, "student_dashboard.html", {"profile": profile})


def is_admin_user(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin_user)
def admin_dashboard(request):
    students = User.objects.filter(is_staff=False).order_by("id")
    registrations, q, status_filter, batch_filter = filtered_registrations(request)
    return render(
        request,
        "admin_dashboard.html",
        {
            "students": students,
            "registrations": registrations,
            "q": q,
            "status_filter": status_filter,
            "batch_filter": batch_filter,
        },
    )


@user_passes_test(is_admin_user)
def export_registrations_csv(request):
    registrations, _, _, _ = filtered_registrations(request)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=student_registrations.csv"

    writer = csv.writer(response)
    writer.writerow(
        [
            "registration_id",
            "submitted_at",
            "full_name",
            "email",
            "contact_number",
            "batch_no",
            "batch_timings",
            "faculty_name",
            "graduation_status",
            "preferred_job_location",
            "application_status",
            "referral_source",
            "account_created",
            "created_user_id",
            "created_username",
        ]
    )

    for reg in registrations:
        writer.writerow(
            [
                reg.id,
                reg.submitted_at.isoformat() if reg.submitted_at else "",
                reg.full_name,
                reg.email,
                reg.contact_number,
                reg.batch_no,
                reg.batch_timings,
                reg.faculty_name,
                reg.graduation_status,
                reg.preferred_job_location,
                reg.application_status,
                reg.referral_source,
                "Yes" if reg.account_created else "No",
                reg.created_user.id if reg.created_user else "",
                reg.created_user.username if reg.created_user else "",
            ]
        )

    return response


@user_passes_test(is_admin_user)
def registration_detail(request, registration_id):
    registration = get_object_or_404(StudentRegistration, id=registration_id)
    display_sections = []
    for section_title, fields in REGISTRATION_SECTIONS:
        rows = []
        for field_name, field_label, _field_type in fields:
            value = getattr(registration, field_name, "")
            rows.append((field_label, value))
        display_sections.append((section_title, rows))

    return render(
        request,
        "registration_detail.html",
        {"registration": registration, "display_sections": display_sections},
    )


@user_passes_test(is_admin_user)
def create_credentials_for_registration(request, registration_id):
    registration = get_object_or_404(StudentRegistration, id=registration_id)

    if registration.account_created and registration.created_user:
        messages.info(
            request,
            f"Credentials already created. User ID: {registration.created_user.id}",
        )
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect(
                "create_credentials_for_registration", registration_id=registration_id
            )

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect(
                "create_credentials_for_registration", registration_id=registration_id
            )

        name_parts = registration.full_name.split(maxsplit=1)
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        user = User.objects.create_user(
            username=username,
            password=password,
            email=registration.email,
            first_name=first_name,
            last_name=last_name,
        )

        StudentProfile.objects.create(
            user=user,
            course_name="Cloud Computing",
            course_duration="TBD",
            progress_percent=0,
            notes=f"Registration ID: {registration.id}",
        )

        registration.account_created = True
        registration.created_user = user
        registration.save()

        messages.success(
            request,
            f"Credentials created for {registration.full_name}. User ID: {user.id}",
        )
        return redirect("admin_dashboard")

    return render(
        request,
        "create_credentials.html",
        {"registration": registration},
    )


@user_passes_test(is_admin_user)
def create_student(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        email = request.POST.get("email", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        course_name = request.POST.get("course_name", "").strip()
        course_duration = request.POST.get("course_duration", "").strip()
        progress_percent = request.POST.get("progress_percent", "0").strip()
        notes = request.POST.get("notes", "").strip()

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect("create_student")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("create_student")

        try:
            progress_value = int(progress_percent)
            if progress_value < 0 or progress_value > 100:
                raise ValueError
        except ValueError:
            messages.error(request, "Progress must be a number between 0 and 100.")
            return redirect("create_student")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        StudentProfile.objects.create(
            user=user,
            course_name=course_name,
            course_duration=course_duration,
            progress_percent=progress_value,
            notes=notes,
        )
        messages.success(request, f"Student created with user ID: {user.id}")
        return redirect("admin_dashboard")

    return render(request, "create_student.html")


@user_passes_test(is_admin_user)
def update_student(request, user_id):
    student_user = get_object_or_404(User, id=user_id, is_staff=False)
    profile, _ = StudentProfile.objects.get_or_create(user=student_user)

    if request.method == "POST":
        student_user.email = request.POST.get("email", "").strip()
        student_user.first_name = request.POST.get("first_name", "").strip()
        student_user.last_name = request.POST.get("last_name", "").strip()
        new_password = request.POST.get("password", "").strip()
        if new_password:
            student_user.set_password(new_password)
        student_user.save()

        profile.course_name = request.POST.get("course_name", "").strip()
        profile.course_duration = request.POST.get("course_duration", "").strip()
        profile.notes = request.POST.get("notes", "").strip()
        try:
            progress_value = int(request.POST.get("progress_percent", "0").strip())
            if progress_value < 0 or progress_value > 100:
                raise ValueError
            profile.progress_percent = progress_value
        except ValueError:
            messages.error(request, "Progress must be between 0 and 100.")
            return redirect("update_student", user_id=user_id)

        profile.save()
        messages.success(request, f"Student data updated for user ID: {student_user.id}")
        return redirect("admin_dashboard")

    return render(
        request,
        "update_student.html",
        {"student_user": student_user, "profile": profile},
    )
