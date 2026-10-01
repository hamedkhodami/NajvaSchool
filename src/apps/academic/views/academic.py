from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.academic.forms import AcademicYearForm
from apps.academic.models import AcademicYearModel
from apps.account.mixins import AdminRequiredMixin


class AcademicYearListView(AdminRequiredMixin, View):
    template_name = "academic/academic_year_list.html"

    def get(self, request):
        years = AcademicYearModel.objects.all()
        return render(request, self.template_name, {"years": years})


class AcademicYearCreateView(AdminRequiredMixin, View):
    template_name = "academic/academic_year_create.html"

    def get(self, request):
        form = AcademicYearForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("academic:academic_year_list")
        return render(request, self.template_name, {"form": form})


class AcademicYearUpdateStatusView(AdminRequiredMixin, View):
    template_name = "academic/academic_year_update_status.html"

    def get(self, request, year_id):
        year = get_object_or_404(AcademicYearModel, id=year_id)
        return render(request, self.template_name, {"year": year})

    def post(self, request, year_id):
        year = get_object_or_404(AcademicYearModel, id=year_id)
        new_status = request.POST.get("status")

        allowed = [
            AcademicYearModel.Status.PLANNED,
            AcademicYearModel.Status.COMPLETED,
        ]

        if new_status in allowed:
            year.status = new_status
            year.save(update_fields=["status"])

        return redirect("academic:academic_year_list")


class AcademicYearActivateView(AdminRequiredMixin, View):
    template_name = "academic/academic_year_activate.html"

    def get(self, request, year_id):
        year = get_object_or_404(AcademicYearModel, id=year_id)
        return render(request, self.template_name, {"year": year})

    def post(self, request, year_id):
        year = get_object_or_404(AcademicYearModel, id=year_id)

        AcademicYearModel.objects.update(status=AcademicYearModel.Status.PLANNED)

        year.status = AcademicYearModel.Status.ACTIVE
        year.save(update_fields=["status"])

        request.session["active_academic_year_id"] = str(year.id)

        return redirect("academic:academic_year_list")
