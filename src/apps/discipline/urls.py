from django.urls import path

from apps.discipline.views import (
    AdminRewardCreateView,
    AdminRewardDeleteView,
    AdminRewardDetailView,
    AdminRewardListView,
    StudentRewardListView,
)


app_name = "discipline"

urlpatterns = [
    path(
        "rewards/",
        AdminRewardListView.as_view(),
        name="admin_reward_list",
    ),
    path(
        "rewards/create/<uuid:classroom_id>/",
        AdminRewardCreateView.as_view(),
        name="admin_reward_create",
    ),
    path(
        "rewards/<uuid:record_id>/",
        AdminRewardDetailView.as_view(),
        name="admin_reward_detail",
    ),
    path(
        "rewards/<uuid:record_id>/delete/",
        AdminRewardDeleteView.as_view(),
        name="admin_reward_delete",
    ),
    path(
        "students/rewards/", StudentRewardListView.as_view(), name="student_reward_list"
    ),
]
