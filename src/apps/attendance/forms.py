from django import forms

from apps.attendance.models import StaffAttendanceModel


class StaffAttendanceForm(forms.ModelForm):
    class Meta:
        model = StaffAttendanceModel
        fields = ["teacher", "status", "description"]
        widgets = {
            "teacher": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-textarea"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["teacher"].label = "معلم"
        self.fields["status"].label = "وضعیت"
        self.fields["description"].label = "توضیحات"
