from django import forms
from django.core.exceptions import ValidationError

from apps.teacher.models import TeacherModel


class TeacherCreationForm(forms.ModelForm):
    class Meta:
        model = TeacherModel
        fields = (
            "national_id",
            "status",
            "employment_type",
            "education",
            "specialization",
        )
        widgets = {
            "national_id": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg",
                }
            ),
            "employment_type": forms.Select(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg",
                }
            ),
            "education": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg",
                }
            ),
            "specialization": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg",
                }
            ),
        }

    def clean_national_id(self):
        national_id = self.cleaned_data["national_id"]

        if TeacherModel.objects.filter(national_id=national_id).exists():
            raise ValidationError("این کد ملی قبلاً ثبت شده است.")

        return national_id
