from django import forms
from django.core.exceptions import ValidationError

from apps.student.models import StudentModel


class StudentCreationForm(forms.ModelForm):
    class Meta:
        model = StudentModel
        fields = (
            "national_id",
            "father_name",
            "parent_phone_number",
            "birth_date",
            "address",
            "status",
        )
        widgets = {
            "national_id": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg",
                }
            ),
            "father_name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg",
                }
            ),
            "parent_phone_number": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg",
                }
            ),
            "birth_date": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg",
                }
            ),
        }

    def clean_national_id(self):
        national_id = self.cleaned_data["national_id"]

        if StudentModel.objects.filter(national_id=national_id).exists():
            raise ValidationError("این کد ملی قبلاً برای یک دانش‌آموز ثبت شده است.")

        return national_id
