from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from apps.academic.forms import AcademicYearForm
from apps.academic.models import AcademicYearModel
from apps.account.mixins import AdminRequiredMixin
from apps.core.pagination import paginate_queryset


class AcademicYearListView(AdminRequiredMixin, View):
    template_name = "academic/academic_year_list.html"

    def get(self, request):
        years = AcademicYearModel.objects.all()
        pagination = paginate_queryset(
            request=request,
            queryset=years,
            per_page=10,
        )

        context = {
            "years": pagination["object_list"],
            "paginator": pagination["paginator"],
            "page_obj": pagination["page_obj"],
            "is_paginated": pagination["is_paginated"],
        }

        return render(request, self.template_name, context)


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


@method_decorator(never_cache, name="dispatch")
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
