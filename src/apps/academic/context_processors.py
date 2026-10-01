from apps.academic.models import AcademicYearModel


def active_academic_year(request):
    year = AcademicYearModel.objects.filter(
        status=AcademicYearModel.Status.ACTIVE
    ).first()
    return {"active_year": year}
