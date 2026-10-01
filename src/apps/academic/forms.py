from django import forms
from khayyam import JalaliDate

from apps.academic.models import AcademicYearModel, ClassroomModel


class AcademicYearForm(forms.ModelForm):
    MONTHS = [(i, f"{i}") for i in range(1, 13)]
    YEARS = [(y, f"{y}") for y in range(1400, 1420)]

    start_month = forms.ChoiceField(choices=MONTHS)
    start_year = forms.ChoiceField(choices=YEARS)

    end_month = forms.ChoiceField(choices=MONTHS)
    end_year = forms.ChoiceField(choices=YEARS)

    class Meta:
        model = AcademicYearModel
        fields = ("name", "status")
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "w-full px-3 py-2 border rounded-lg text-sm"}
            ),
            "status": forms.Select(
                attrs={"class": "w-full px-3 py-2 border rounded-lg text-sm"}
            ),
        }

    def clean(self):
        cleaned = super().clean()

        sm = int(cleaned["start_month"])
        sy = int(cleaned["start_year"])

        em = int(cleaned["end_month"])
        ey = int(cleaned["end_year"])

        cleaned["start_date"] = JalaliDate(sy, sm, 1).todate()
        cleaned["end_date"] = JalaliDate(ey, em, 1).todate()

        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.start_date = self.cleaned_data["start_date"]
        obj.end_date = self.cleaned_data["end_date"]
        if commit:
            obj.save()
        return obj


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = ClassroomModel
        fields = ["grade", "name", "capacity", "status"]

    def init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["grade"].label = "پایه تحصیلی"
        self.fields["name"].label = "نام کلاس"
        self.fields["capacity"].label = "ظرفیت"
        self.fields["status"].label = "وضعیت"
