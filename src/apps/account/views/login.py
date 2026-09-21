from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from apps.account import forms
from apps.account.mixins import LogoutRequiredMixin
from apps.core.utils import toast_form_errors


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("account:login")


class LoginView(LogoutRequiredMixin, FormView):
    template_name = "account/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("public:home")

    def remember_me(self, form):
        if not form.cleaned_data.get("remember_me"):
            self.request.session.set_expiry(0)
            self.request.session.modified = True

    def form_valid(self, form):
        user = form.cleaned_data["user"]

        if not user.is_verified:
            self.request.session["verify_user_id"] = user.id

            return redirect("account:send_code")

        login(self.request, user)
        self.remember_me(form)

        messages.success(
            self.request,
            "ورود با موفقیت انجام شد.",
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)
