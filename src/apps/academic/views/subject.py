from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from apps.academic.forms import SubjectForm
from apps.academic.models import SubjectModel
from apps.account.mixins import AdminRequiredMixin
from apps.core.pagination import paginate_queryset


class SubjectListView(AdminRequiredMixin, View):
    template_name = "academic/subject/subject_list.html"

    def get(self, request):
        subjects = SubjectModel.objects.filter(is_deleted=False)
        pagination = paginate_queryset(
            request=request,
            queryset=subjects,
            per_page=10,
        )

        context = {
            "subjects": pagination["object_list"],
            "paginator": pagination["paginator"],
            "page_obj": pagination["page_obj"],
            "is_paginated": pagination["is_paginated"],
        }

        return render(request, self.template_name, context)


class SubjectCreateView(AdminRequiredMixin, View):
    template_name = "academic/subject/subject_create.html"

    def get(self, request):
        form = SubjectForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SubjectForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "درس جدید با موفقیت ثبت شد.")
            return redirect("academic:subject_list")

        messages.error(request, "اطلاعات وارد شده معتبر نیست.")
        return render(request, self.template_name, {"form": form})


@method_decorator(never_cache, name="dispatch")
class SubjectUpdateView(AdminRequiredMixin, View):
    template_name = "academic/subject/subject_update.html"

    def get(self, request, subject_id):
        subject = get_object_or_404(SubjectModel, id=subject_id)
        form = SubjectForm(instance=subject)
        return render(request, self.template_name, {"form": form, "subject": subject})

    def post(self, request, subject_id):
        subject = get_object_or_404(SubjectModel, id=subject_id)
        form = SubjectForm(request.POST, instance=subject)

        if form.is_valid():
            form.save()
            messages.success(request, "درس با موفقیت بروزرسانی شد.")
            return redirect("academic:subject_list")

        messages.error(request, "اطلاعات وارد شده معتبر نیست.")
        return render(request, self.template_name, {"form": form, "subject": subject})


class SubjectDeleteView(AdminRequiredMixin, View):
    template_name = "academic/subject/subject_delete.html"

    def get(self, request, subject_id):
        subject = get_object_or_404(SubjectModel, id=subject_id)
        return render(request, self.template_name, {"subject": subject})

    def post(self, request, subject_id):
        subject = get_object_or_404(SubjectModel, id=subject_id)
        subject.delete()  # SoftDelete
        messages.success(request, "درس با موفقیت حذف شد.")
        return redirect("academic:subject_list")
