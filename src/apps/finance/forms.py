from decimal import Decimal

from django import forms

from apps.finance.models import (
    PaymentRecordModel,
    SalaryPaymentModel,
    SchoolExpenseModel,
    StaffSalaryModel,
    TuitionModel,
)


class TuitionCreateForm(forms.ModelForm):
    discount_percent = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=100,
        initial=0,
        label="درصد تخفیف",
        widget=forms.NumberInput(attrs={"class": "border p-2 rounded w-full"}),
    )

    class Meta:
        model = TuitionModel
        fields = [
            "student",
            "academic_year",
            "amount",
            "description",
        ]

        widgets = {
            "student": forms.Select(attrs={"class": "border p-2 rounded w-full"}),
            "academic_year": forms.Select(attrs={"class": "border p-2 rounded w-full"}),
            "amount": forms.NumberInput(attrs={"class": "border p-2 rounded w-full"}),
            "description": forms.Textarea(attrs={"class": "border p-2 rounded w-full"}),
        }

    def clean(self):
        cleaned = super().clean()

        student = cleaned.get("student")
        academic_year = cleaned.get("academic_year")
        amount = cleaned.get("amount")

        if student and academic_year:
            if TuitionModel.objects.filter(
                student=student,
                academic_year=academic_year,
            ).exists():
                raise forms.ValidationError(
                    "برای این دانش‌آموز در این سال تحصیلی " "قبلاً شهریه ثبت شده است."
                )

        discount_percent = cleaned.get("discount_percent") or 0

        if amount is not None:
            cleaned["discount"] = amount * Decimal(discount_percent) / Decimal("100")

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.discount = self.cleaned_data.get("discount", Decimal("0"))

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class StaffSalaryUpdateForm(forms.ModelForm):
    class Meta:
        model = StaffSalaryModel
        fields = ["academic_year", "base_amount", "description"]

        widgets = {
            "academic_year": forms.Select(attrs={"class": "border p-2 rounded w-full"}),
            "base_amount": forms.NumberInput(
                attrs={"class": "border p-2 rounded w-full"}
            ),
            "description": forms.Textarea(attrs={"class": "border p-2 rounded w-full"}),
        }

    def clean(self):
        cleaned = super().clean()

        academic_year = cleaned.get("academic_year")
        teacher = self.instance.teacher

        # جلوگیری از ثبت حکم تکراری برای سال دیگر
        exists = (
            StaffSalaryModel.objects.filter(
                teacher=teacher, academic_year=academic_year
            )
            .exclude(id=self.instance.id)
            .exists()
        )

        if exists:
            raise forms.ValidationError(
                f"برای این معلم در سال تحصیلی {academic_year.name} قبلاً حکم ثبت شده است."
            )

        return cleaned


class PaymentCreateForm(forms.ModelForm):
    class Meta:
        model = PaymentRecordModel
        fields = ["amount", "payment_method", "description"]

        widgets = {
            "amount": forms.NumberInput(attrs={"class": "border p-2 rounded w-full"}),
            "payment_method": forms.Select(
                attrs={"class": "border p-2 rounded w-full"}
            ),
            "description": forms.Textarea(attrs={"class": "border p-2 rounded w-full"}),
        }

    def __init__(self, *args, **kwargs):
        # گرفتن شهریه از ویو
        self.tuition = kwargs.pop("tuition", None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        if self.tuition:
            remaining = self.tuition.remaining_amount

            if amount > remaining:
                raise forms.ValidationError(
                    f"مبلغ پرداخت ({amount:,}) نمی‌تواند بیشتر از مبلغ باقی‌مانده ({remaining:,}) باشد."
                )

        return amount


class StaffSalaryCreateForm(forms.ModelForm):

    class Meta:
        model = StaffSalaryModel
        fields = [
            "teacher",
            "academic_year",
            "base_amount",
            "description",
        ]

        widgets = {
            "teacher": forms.Select(attrs={"class": "border p-2 rounded w-full"}),
            "academic_year": forms.Select(attrs={"class": "border p-2 rounded w-full"}),
            "base_amount": forms.NumberInput(
                attrs={"class": "border p-2 rounded w-full"}
            ),
            "description": forms.Textarea(attrs={"class": "border p-2 rounded w-full"}),
        }

    def clean(self):
        cleaned = super().clean()

        teacher = cleaned.get("teacher")
        academic_year = cleaned.get("academic_year")

        # جلوگیری از ثبت حقوق تکراری برای یک سال تحصیلی
        if teacher and academic_year:
            if StaffSalaryModel.objects.filter(
                teacher=teacher,
                academic_year=academic_year,
            ).exists():
                raise forms.ValidationError(
                    f"برای این معلم در سال تحصیلی {academic_year.name} قبلاً حقوق ثبت شده است."
                )

        return cleaned


class SalaryPaymentCreateForm(forms.ModelForm):
    class Meta:
        model = SalaryPaymentModel
        fields = ["amount", "description"]

        widgets = {
            "amount": forms.NumberInput(attrs={"class": "border p-2 rounded w-full"}),
            "description": forms.Textarea(attrs={"class": "border p-2 rounded w-full"}),
        }

    def __init__(self, *args, **kwargs):
        self.salary = kwargs.pop("salary", None)
        super().__init__(*args, **kwargs)

        if self.salary:
            self.fields["amount"].initial = self.salary.base_amount


class SchoolExpenseCreateForm(forms.ModelForm):
    class Meta:
        model = SchoolExpenseModel
        fields = ["academic_year", "title", "category", "amount", "description"]

        widgets = {
            "academic_year": forms.Select(attrs={"class": "border p-2 rounded w-full"}),
            "title": forms.TextInput(attrs={"class": "border p-2 rounded w-full"}),
            "category": forms.Select(attrs={"class": "border p-2 rounded w-full"}),
            "amount": forms.NumberInput(attrs={"class": "border p-2 rounded w-full"}),
            "description": forms.Textarea(attrs={"class": "border p-2 rounded w-full"}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount <= 0:
            raise forms.ValidationError("مبلغ باید بزرگ‌تر از صفر باشد.")
        return amount


class SchoolExpenseUpdateForm(forms.ModelForm):
    class Meta:
        model = SchoolExpenseModel
        fields = ["academic_year", "title", "category", "amount", "description"]

        widgets = {
            "academic_year": forms.Select(attrs={"class": "border p-2 rounded w-full"}),
            "title": forms.TextInput(attrs={"class": "border p-2 rounded w-full"}),
            "category": forms.Select(attrs={"class": "border p-2 rounded w-full"}),
            "amount": forms.NumberInput(attrs={"class": "border p-2 rounded w-full"}),
            "description": forms.Textarea(attrs={"class": "border p-2 rounded w-full"}),
        }
