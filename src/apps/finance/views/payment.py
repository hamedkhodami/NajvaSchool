from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.finance.forms import PaymentCreateForm
from apps.finance.models import TuitionModel


class TuitionPaymentCreateView(View):
    template_name = "finance/payment/create.html"

    def get(self, request, tuition_id):
        tuition = get_object_or_404(TuitionModel, id=tuition_id)
        form = PaymentCreateForm(tuition=tuition)
        return render(request, self.template_name, {"form": form, "tuition": tuition})

    def post(self, request, tuition_id):
        tuition = get_object_or_404(TuitionModel, id=tuition_id)
        form = PaymentCreateForm(request.POST, tuition=tuition)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = tuition.student
            payment.tuition = tuition
            payment.save()  # 🔥 اینجا created_at اتوماتیک ثبت می‌شود

            tuition.update_status()

            return redirect("finance:tuition_detail", tuition_id=tuition.id)

        return render(request, self.template_name, {"form": form, "tuition": tuition})
