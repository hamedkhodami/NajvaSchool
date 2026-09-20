from random import randint

from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from apps.account import forms
from apps.account.mixins import LogoutRequiredMixin
from apps.account.models import User
from apps.account.services.otp_service import OTPService
from apps.core.utils import toast_form_errors


class SendCodeView(LogoutRequiredMixin, View):
    def get_redirect_url(self):
        return self.request.GET.get(
            "next",
            reverse("account:reset_pass_confirm"),
        )

    def get(self, request):
        user_id = request.session.get("reset_user_id")

        if not user_id:
            messages.error(
                request,
                "نشست شما منقضی شده است. لطفاً دوباره تلاش کنید.",
            )
            return redirect("account:get_phone_number")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(
                request,
                "خطایی رخ داده است. لطفاً دوباره تلاش کنید.",
            )
            return redirect("account:get_phone_number")

        if not OTPService.can_send(user.phone_number):
            messages.warning(
                request,
                "لطفاً قبل از درخواست کد جدید کمی صبر کنید.",
            )
            return redirect(self.get_redirect_url())

        code = randint(100000, 999999)

        OTPService.set_otp(
            user.phone_number,
            str(code),
        )

        # TODO: notifications

        messages.info(
            request,
            "کد تأیید برای شما ارسال شد.",
        )

        return redirect(self.get_redirect_url())


class GetPhoneNumberView(LogoutRequiredMixin, FormView):
    template_name = "account/password/get_phone.html"
    form_class = forms.GetPhoneNumberForm

    def get_success_url(self):
        return (
            reverse("account:send_code")
            + f'?next={reverse("account:reset_pass_confirm")}'
        )

    def form_valid(self, form):
        user = form.cleaned_data["user"]

        self.request.session["reset_user_id"] = user.id

        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class ResetPassConfirmView(LogoutRequiredMixin, FormView):
    template_name = "account/password/reset_pass_confirm.html"
    form_class = forms.VerifyPhoneNumberForm
    success_url = reverse_lazy("account:reset_pass_complete")

    def form_valid(self, form):
        code = form.cleaned_data["code"]

        user_id = self.request.session.get("reset_user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(
                self.request,
                "خطایی رخ داده است. لطفاً دوباره تلاش کنید.",
            )
            return redirect("account:get_phone_number")

        if not OTPService.verify_otp(
            user.phone_number,
            code,
        ):
            messages.error(
                self.request,
                "کد واردشده صحیح نیست.",
            )
            return redirect("account:reset_pass_confirm")

        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class ResetPassCompleteView(LogoutRequiredMixin, FormView):
    template_name = "account/password/reset_pass_complete.html"
    form_class = forms.ResetPassForm
    success_url = reverse_lazy("account:login")

    def form_valid(self, form):
        password = form.cleaned_data.get("password2")
        user_id = self.request.session.get("reset_user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(
                self.request,
                "خطایی رخ داده است. لطفاً دوباره تلاش کنید.",
            )
            return self.form_invalid(form)

        user.set_password(password)
        user.is_verified = True
        user.save()

        self.request.session.pop("reset_user_id", None)

        messages.success(
            self.request,
            "رمز عبور با موفقیت تغییر کرد.",
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)