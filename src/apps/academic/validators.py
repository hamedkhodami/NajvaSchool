from apps.academic.models import ClassroomModel


def validate_student_enrollment(student, classroom):
    if classroom.students.filter(id=student.id).exists():
        return "این دانش‌آموز از قبل در این کلاس وجود دارد."

    other_class = (
        ClassroomModel.objects.filter(
            students=student, academic_year=classroom.academic_year
        )
        .exclude(id=classroom.id)
        .first()
    )

    if other_class:
        return f"این دانش‌آموز در کلاس دیگری ({other_class.name}) از همین سال تحصیلی ثبت‌نام شده است."

    return None
