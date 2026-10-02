from django import forms
from khayyam import JalaliDate

from apps.academic.models import (
    AcademicYearModel,
    ClassroomModel,
    ScheduleSessionModel,
    SubjectModel,
)
from apps.academic.validators import validate_student_enrollment
from apps.student.models import StudentModel
from apps.teacher.models import TeacherModel


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["grade"].label = "پایه تحصیلی"
        self.fields["name"].label = "نام کلاس"
        self.fields["capacity"].label = "ظرفیت"
        self.fields["status"].label = "وضعیت"


class ClassroomStudentForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=StudentModel.objects.filter(is_deleted=False),
        label="دانش‌آموز",
    )

    def __init__(self, classroom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classroom = classroom

    def clean_student(self):
        student = self.cleaned_data["student"]

        if self.classroom.students.count() >= self.classroom.capacity:
            raise forms.ValidationError(
                "ظرفیت کلاس تکمیل شده است و امکان افزودن دانش‌آموز جدید وجود ندارد."
            )

        error = validate_student_enrollment(student, self.classroom)
        if error:
            raise forms.ValidationError(error)

        return student


class SubjectForm(forms.ModelForm):
    class Meta:
        model = SubjectModel
        fields = ["name", "code", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "نام درس"
        self.fields["code"].label = "کد درس"
        self.fields["description"].label = "توضیحات"


class ScheduleSessionForm(forms.ModelForm):
    class Meta:
        model = ScheduleSessionModel
        fields = ["subject", "teacher", "weekday", "session_number"]

    def __init__(self, classroom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classroom = classroom

        self.fields["subject"].queryset = SubjectModel.objects.filter(is_deleted=False)
        self.fields["teacher"].queryset = TeacherModel.objects.filter(is_deleted=False)

    def clean(self):
        cleaned_data = super().clean()
        weekday = cleaned_data.get("weekday")
        session_number = cleaned_data.get("session_number")

        if (
            ScheduleSessionModel.objects.filter(
                classroom=self.classroom, weekday=weekday, session_number=session_number
            )
            .exclude(id=self.instance.id)
            .exists()
        ):
            raise forms.ValidationError(
                "این شماره جلسه در این روز برای این کلاس از قبل ثبت شده است."
            )

        if (
            ScheduleSessionModel.objects.filter(
                teacher=cleaned_data.get("teacher"),
                weekday=weekday,
                session_number=session_number,
            )
            .exclude(id=self.instance.id)
            .exists()
        ):
            raise forms.ValidationError(
                "این معلم در همین بازه زمانی در کلاس دیگری حضور دارد."
            )

        return cleaned_data
