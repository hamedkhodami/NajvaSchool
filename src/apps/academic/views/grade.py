from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.academic.forms import ClassroomForm
from apps.academic.models import ClassroomModel
from apps.academic.services.active_year import get_active_year
from apps.account.mixins import AdminRequiredMixin


class ClassroomListView(AdminRequiredMixin, View):
    template_name = "academic/grade/classroom_list.html"

    def get(self, request):
        active_year = get_active_year(request)

        if not active_year:
            classrooms = ClassroomModel.objects.none()
        else:
            classrooms = ClassroomModel.objects.filter(
                academic_year=active_year, is_deleted=False
            )

        return render(
            request,
            self.template_name,
            {
                "classrooms": classrooms,
                "active_year": active_year,
            },
        )


class ClassroomCreateView(AdminRequiredMixin, View):
    template_name = "academic/grade/classroom_create.html"

    def get(self, request):
        form = ClassroomForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ClassroomForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.academic_year = get_active_year(request)
            obj.save()
            return redirect("academic:classroom_list")

        return render(request, self.template_name, {"form": form})


class ClassroomUpdateView(AdminRequiredMixin, View):
    template_name = "academic/grade/classroom_update.html"

    def get(self, request, class_id):
        obj = get_object_or_404(ClassroomModel, id=class_id)
        form = ClassroomForm(instance=obj)
        return render(request, self.template_name, {"form": form, "obj": obj})

    def post(self, request, class_id):
        obj = get_object_or_404(ClassroomModel, id=class_id)
        form = ClassroomForm(request.POST, instance=obj)

        if form.is_valid():
            form.save()
            return redirect("academic:classroom_list")

        return render(request, self.template_name, {"form": form, "obj": obj})


class ClassroomDeleteView(AdminRequiredMixin, View):
    template_name = "academic/grade/classroom_delete.html"

    def get(self, request, class_id):
        obj = get_object_or_404(ClassroomModel, id=class_id)
        return render(request, self.template_name, {"obj": obj})

    def post(self, request, class_id):
        obj = get_object_or_404(ClassroomModel, id=class_id)
        obj.delete()
        return redirect("academic:classroom_list")
