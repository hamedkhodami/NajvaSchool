from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from apps.academic.models import AcademicYearModel
from apps.finance.forms import SchoolExpenseCreateForm, SchoolExpenseUpdateForm
from apps.finance.models import SchoolExpenseModel


class ExpenseListView(View):
    template_name = "finance/expense/list.html"

    def get(self, request):
        year_id = request.GET.get("year")
        search = request.GET.get("search")

        expenses = SchoolExpenseModel.objects.select_related("academic_year").filter(
            is_deleted=False
        )

        if year_id:
            expenses = expenses.filter(academic_year_id=year_id)

        if search:
            expenses = expenses.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        years = AcademicYearModel.objects.all()

        return render(
            request,
            self.template_name,
            {
                "expenses": expenses,
                "years": years,
            },
        )


class ExpenseCreateView(View):
    template_name = "finance/expense/create.html"

    def get(self, request):
        form = SchoolExpenseCreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SchoolExpenseCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("finance:expense_list")
        return render(request, self.template_name, {"form": form})


class ExpenseUpdateView(View):
    template_name = "finance/expense/update.html"

    def get(self, request, expense_id):
        expense = get_object_or_404(SchoolExpenseModel, id=expense_id)
        form = SchoolExpenseUpdateForm(instance=expense)
        return render(request, self.template_name, {"form": form, "expense": expense})

    def post(self, request, expense_id):
        expense = get_object_or_404(SchoolExpenseModel, id=expense_id)
        form = SchoolExpenseUpdateForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("finance:expense_list")
        return render(request, self.template_name, {"form": form, "expense": expense})


class ExpenseDeleteView(View):
    def post(self, request, expense_id):
        expense = get_object_or_404(SchoolExpenseModel, id=expense_id)
        expense.is_deleted = True
        expense.deleted_at = timezone.now()
        expense.save(update_fields=["is_deleted", "deleted_at"])
        return redirect("finance:expense_list")
