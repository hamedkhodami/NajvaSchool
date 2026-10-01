from django.urls import path

from apps.student.views import admin, student


app_name = "student"

urlpatterns = [
    # student
    path("profile/", student.StudentProfileView.as_view(), name="profile"),
    # admin
    path("create/", admin.CreateStudentUserView.as_view(), name="create_student"),
    path("list/", admin.StudentListView.as_view(), name="list"),
    path("detail/<uuid:pk>/", admin.StudentDetailView.as_view(), name="detail"),
]
