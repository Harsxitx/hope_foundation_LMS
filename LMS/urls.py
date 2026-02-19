from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("student/register/", views.student_register_view, name="student_register"),
    path("student/login/", views.student_login_view, name="student_login"),
    path("admin/login/", views.admin_login_view, name="admin_login"),
    path("logout/", views.logout_view, name="logout"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path(
        "admin/registrations/export-csv/",
        views.export_registrations_csv,
        name="export_registrations_csv",
    ),
    path("admin/students/create/", views.create_student, name="create_student"),
    path("admin/students/<int:user_id>/update/", views.update_student, name="update_student"),
    path(
        "admin/registrations/<int:registration_id>/",
        views.registration_detail,
        name="registration_detail",
    ),
    path(
        "admin/registrations/<int:registration_id>/create-credentials/",
        views.create_credentials_for_registration,
        name="create_credentials_for_registration",
    ),
]
