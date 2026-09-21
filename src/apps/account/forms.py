from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from persian_tools import digits

from apps.account.models import User
from apps.account.utils import check_phone_number


class UserCreationForm(forms.ModelForm):
    phone_number = forms.CharField(
        label="شماره موبایل",
        max_length=11,
    )

    first_name = forms.CharField(
        label="نام",
        max_length=128,
    )

    last_name = forms.CharField(
        label="نام خانوادگی",
        max_length=128,
    )

    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
            "last_name",
            "role",
        )

    def clean_phone_number(self):
        phone_number = digits.convert_to_en(self.cleaned_data.get("phone_number"))

        if not check_phone_number(phone_number):
            raise ValidationError("شماره موبایل واردشده معتبر نیست.")

        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("این شماره موبایل قبلاً ثبت شده است.")

        return phone_number

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("رمزهای عبور یکسان نیستند.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        label="شماره موبایل",
        max_length=11,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "09__",
            }
        ),
    )

    password = forms.CharField(
        label="رمز عبور",
        max_length=128,
        required=True,
        widget=forms.PasswordInput(),
    )

    remember_me = forms.BooleanField(
        label="مرا به خاطر بسپار",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        phone = cleaned_data.get("phone_number")
        password = cleaned_data.get("password")

        if not phone or not password:
            return cleaned_data

        phone = digits.convert_to_en(phone)

        if not check_phone_number(phone):
            raise ValidationError(
                "شماره موبایل واردشده معتبر نیست.",
                code="BAD-PHONE",
            )

        user = authenticate(
            username=phone,
            password=password,
        )

        if not user:
            raise ValidationError(
                "شماره موبایل یا رمز عبور اشتباه است.",
                code="INVALID-CREDENTIALS",
            )

        cleaned_data["phone_number"] = phone
        cleaned_data["user"] = user

        return cleaned_data


class VerifyPhoneNumberForm(forms.Form):
    code = forms.CharField(
        label="کد تأیید",
        max_length=6,
        required=True,
        widget=forms.NumberInput(),
    )

    def clean_code(self):
        code = self.cleaned_data.get("code")

        if not code.isdigit():
            raise ValidationError("کد تأیید واردشده معتبر نیست.")

        return code


class GetPhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        label="شماره موبایل",
        max_length=11,
        widget=forms.TextInput(
            attrs={
                "placeholder": "09__",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        phone_number = cleaned_data.get("phone_number")

        if not phone_number:
            return cleaned_data

        phone_number = digits.convert_to_en(phone_number)

        if not check_phone_number(phone_number):
            raise ValidationError(
                "شماره موبایل واردشده معتبر نیست.",
                code="BAD-PHONE-NUMBER",
            )

        try:
            user = User.objects.get(
                phone_number=phone_number,
            )
        except User.DoesNotExist as error:
            raise ValidationError("کاربری با این شماره موبایل پیدا نشد.") from error

        cleaned_data["phone_number"] = phone_number
        cleaned_data["user"] = user

        return cleaned_data


class ResetPassForm(forms.Form):
    password = forms.CharField(
        label="رمز عبور جدید",
        max_length=128,
        min_length=4,
        required=True,
        widget=forms.PasswordInput(),
    )

    password2 = forms.CharField(
        label="تکرار رمز عبور جدید",
        max_length=128,
        min_length=4,
        required=True,
        widget=forms.PasswordInput(),
    )

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise ValidationError("رمزهای عبور یکسان نیستند.")

        return password2
