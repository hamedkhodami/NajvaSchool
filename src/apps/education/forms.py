from django import forms

from apps.academic.models import ClassroomModel, SubjectModel
from apps.education.models import ExamModel


class ExamCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop("teacher", None)
        active_year = kwargs.pop("active_year", None)
        super().__init__(*args, **kwargs)

        # فقط کلاس‌هایی که معلم در سال فعال تدریس می‌کند
        if teacher and active_year:
            self.fields["classroom"].queryset = ClassroomModel.objects.filter(
                schedule_sessions__teacher=teacher, academic_year=active_year
            ).distinct()

        # درس‌ها (در صورت نیاز می‌توانیم بر اساس کلاس فیلتر کنیم)
        self.fields["subject"].queryset = SubjectModel.objects.all()

    class Meta:
        model = ExamModel
        fields = [
            "classroom",
            "subject",
            "description",
            "max_score",
            "duration",
            "file",
        ]


class ExamUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop("teacher", None)
        active_year = kwargs.pop("active_year", None)
        super().__init__(*args, **kwargs)

        # فقط کلاس‌های سال فعال که معلم تدریس می‌کند
        if teacher and active_year:
            self.fields["classroom"].queryset = ClassroomModel.objects.filter(
                schedule_sessions__teacher=teacher, academic_year=active_year
            ).distinct()

        self.fields["subject"].queryset = SubjectModel.objects.all()

    class Meta:
        model = ExamModel
        fields = [
            "classroom",
            "subject",
            "description",
            "max_score",
            "duration",
            "file",
            "is_published",
        ]
