from django.shortcuts import redirect, render
from django.views import View

from apps.academic.forms import AcademicYearForm
from apps.academic.models import AcademicYearModel
from apps.account.mixins import AdminRequiredMixin


class AcademicYearListCreateView(AdminRequiredMixin, View):
    template_name = "academic/academic_year_list.html"

    def get(self, request):
        years = AcademicYearModel.objects.all()
        form = AcademicYearForm()
        return render(
            request,
            self.template_name,
            {
                "years": years,
                "form": form,
            },
        )

    def post(self, request):
        form = AcademicYearForm(request.POST)

        if not form.is_valid():
            years = AcademicYearModel.objects.all()
            return render(
                request,
                self.template_name,
                {
                    "years": years,
                    "form": form,
                },
            )

        form.save()
        return redirect("academic:academic_year_list")
