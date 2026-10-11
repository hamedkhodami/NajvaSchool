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
        widgets = {
            "grade": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "capacity": forms.NumberInput(attrs={"class": "form-input"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

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
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, classroom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classroom = classroom

    def clean_student(self):
        student = self.cleaned_data["student"]

        # ظرفیت کلاس
        if self.classroom.students.count() >= self.classroom.capacity:
            raise forms.ValidationError("ظرفیت کلاس تکمیل شده است.")

        # ولیدیشن‌های قبلی
        error = validate_student_enrollment(student, self.classroom)
        if error:
            raise forms.ValidationError(error)

        # جلوگیری از ثبت دانش‌آموز در دو کلاس یک سال تحصیلی
        if student.classrooms.filter(
            academic_year=self.classroom.academic_year
        ).exists():
            raise forms.ValidationError(
                "این دانش‌آموز در کلاس دیگری از همین سال تحصیلی ثبت‌نام شده است."
            )

        return student


class SubjectForm(forms.ModelForm):
    class Meta:
        model = SubjectModel
        fields = ["name", "code", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "code": forms.Select(attrs={"class": "form-select"}),  # اصلاح شد
            "description": forms.Textarea(attrs={"class": "form-textarea"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "نام درس"
        self.fields["code"].label = "پایه درس"
        self.fields["description"].label = "توضیحات"


class ScheduleSessionForm(forms.ModelForm):
    class Meta:
        model = ScheduleSessionModel
        fields = ["subject", "teacher", "weekday", "session_number"]
        widgets = {
            "subject": forms.Select(attrs={"class": "form-select"}),
            "teacher": forms.Select(attrs={"class": "form-select"}),
            "weekday": forms.Select(attrs={"class": "form-select"}),
            "session_number": forms.NumberInput(attrs={"class": "form-input"}),
        }

    def __init__(self, classroom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classroom = classroom

        self.fields["subject"].queryset = SubjectModel.objects.filter(is_deleted=False)
        self.fields["teacher"].queryset = TeacherModel.objects.filter(is_deleted=False)

        self.fields["subject"].label = "درس"
        self.fields["teacher"].label = "معلم"
        self.fields["weekday"].label = "روز هفته"
        self.fields["session_number"].label = "شماره زنگ"

    def clean(self):
        cleaned_data = super().clean()
        weekday = cleaned_data.get("weekday")
        session_number = cleaned_data.get("session_number")

        # جلوگیری از جلسهٔ تکراری
        if (
            ScheduleSessionModel.objects.filter(
                classroom=self.classroom,
                weekday=weekday,
                session_number=session_number,
            )
            .exclude(id=self.instance.id)
            .exists()
        ):
            raise forms.ValidationError("این زنگ در این روز از قبل ثبت شده است.")

        # جلوگیری از تداخل معلم
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
                "این معلم در همین زمان در کلاس دیگری حضور دارد."
            )

        return cleaned_data
