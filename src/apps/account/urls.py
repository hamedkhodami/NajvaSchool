from django.urls import path

from apps.account.views import login, password, user


app_name = "account"

urlpatterns = [
    path(
        "login/",
        login.LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        login.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "password/reset/",
        password.GetPhoneNumberView.as_view(),
        name="get_phone_number",
    ),
    path(
        "password/reset/send-code/",
        password.SendCodeView.as_view(),
        name="send_code",
    ),
    path(
        "password/reset/confirm/",
        password.ResetPassConfirmView.as_view(),
        name="reset_pass_confirm",
    ),
    path(
        "password/reset/complete/",
        password.ResetPassCompleteView.as_view(),
        name="reset_pass_complete",
    ),
    path("users/", user.UserListView.as_view(), name="user_list"),
    path("users/<uuid:pk>/", user.UserDetailView.as_view(), name="user_detail"),
]
