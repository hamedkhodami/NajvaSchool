from django.urls import path

from apps.teacher.views import admin, teacher


app_name = "teacher"

urlpatterns = [
    # admin
    path("create/", admin.CreateTeacherUserView.as_view(), name="create_teacher"),
    path("list/", admin.TeacherListView.as_view(), name="list"),
    path("detail/<uuid:pk>/", admin.TeacherDetailView.as_view(), name="detail"),
    # teacher
    path("profile/", teacher.TeacherProfileView.as_view(), name="profile"),
]
