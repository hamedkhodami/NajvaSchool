from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.academic.models import AcademicYearModel
from apps.academic.services.active_year import get_active_year
from apps.finance.forms import TuitionCreateForm
from apps.finance.models import TuitionModel


class TuitionCreateView(View):
    template_name = "finance/tuition/create.html"

    def get(self, request):
        form = TuitionCreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = TuitionCreateForm(request.POST)

        if form.is_valid():
            tuition = form.save()
            print("TUITION SAVED:", tuition.pk)
            return redirect("finance:tuition_list")

        print("FORM ERRORS:", form.errors)
        print("FORM NON FIELD ERRORS:", form.non_field_errors())
        print("POST DATA:", request.POST.dict())

        return render(request, self.template_name, {"form": form})


class TuitionListView(View):
    template_name = "finance/tuition/list.html"

    def get(self, request):
        # فیلترها
        year_id = request.GET.get("year")
        status = request.GET.get("status")
        search = request.GET.get("search")

        tuitions = TuitionModel.objects.select_related("student", "academic_year")

        # فیلتر سال تحصیلی
        if year_id:
            tuitions = tuitions.filter(academic_year_id=year_id)

        # فیلتر وضعیت
        if status:
            tuitions = tuitions.filter(status=status)

        # جستجو دانش‌آموز
        if search:
            tuitions = tuitions.filter(
                Q(student__user__first_name__icontains=search)
                | Q(student__user__last_name__icontains=search)
                | Q(student__national_id__icontains=search)
                | Q(student__user__phone_number__icontains=search)
            )

        years = AcademicYearModel.objects.all()

        return render(
            request,
            self.template_name,
            {
                "tuitions": tuitions,
                "years": years,
            },
        )


class TuitionDetailView(View):
    template_name = "finance/tuition/detail.html"

    def get(self, request, tuition_id):
        tuition = get_object_or_404(TuitionModel, id=tuition_id)

        payments = tuition.payments.order_by("created_at")

        for index, p in enumerate(payments, start=1):
            p.installment_number = index

        return render(
            request,
            self.template_name,
            {
                "tuition": tuition,
                "payments": payments,
            },
        )


class StudentTuitionStatusView(View):
    template_name = "student/tuition_status.html"

    def get(self, request):
        student = request.user.student
        active_year = get_active_year(request)

        tuition = None
        payments = []

        if active_year:
            tuition = TuitionModel.objects.filter(
                student=student, academic_year=active_year
            ).first()

            if tuition:
                payments = tuition.payments.order_by("created_at")

                # شماره‌گذاری اقساط
                for index, p in enumerate(payments, start=1):
                    p.installment_number = index

        return render(
            request,
            self.template_name,
            {
                "tuition": tuition,
                "payments": payments,
                "active_year": active_year,
            },
        )
