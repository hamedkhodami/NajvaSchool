from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.academic.forms import SubjectForm
from apps.academic.models import SubjectModel
from apps.account.mixins import AdminRequiredMixin


class SubjectListView(AdminRequiredMixin, View):
    template_name = "academic/subject/subject_list.html"

    def get(self, request):
        subjects = SubjectModel.objects.filter(is_deleted=False)
        return render(request, self.template_name, {"subjects": subjects})


class SubjectCreateView(AdminRequiredMixin, View):
    template_name = "academic/subject/subject_create.html"

    def get(self, request):
        form = SubjectForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SubjectForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("academic:subject_list")
        return render(request, self.template_name, {"form": form})


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
            return redirect("academic:subject_list")

        return render(request, self.template_name, {"form": form, "subject": subject})


class SubjectDeleteView(AdminRequiredMixin, View):
    template_name = "academic/subject/subject_delete.html"

    def get(self, request, subject_id):
        subject = get_object_or_404(SubjectModel, id=subject_id)
        return render(request, self.template_name, {"subject": subject})

    def post(self, request, subject_id):
        subject = get_object_or_404(SubjectModel, id=subject_id)
        subject.delete()  # SoftDelete
        return redirect("academic:subject_list")
