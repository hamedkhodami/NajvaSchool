from apps.academic.models import AcademicYearModel


def get_active_year(request):
    year = AcademicYearModel.objects.filter(
        status=AcademicYearModel.Status.ACTIVE
    ).first()
    if year:
        return year

    year_id = request.session.get("active_academic_year_id")
    if year_id:
        return AcademicYearModel.objects.filter(id=year_id).first()

    return None
