from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.academic.forms import ClassroomForm, ClassroomStudentForm
from apps.academic.models import ClassroomModel
from apps.academic.services.active_year import get_active_year
from apps.account.mixins import AdminRequiredMixin
from apps.student.models import StudentModel


class ClassroomListView(AdminRequiredMixin, View):
    template_name = "academic/grade/classroom_list.html"

    def get(self, request):
        active_year = get_active_year(request)

        if not active_year:
            messages.error(request, "هیچ سال تحصیلی فعالی وجود ندارد.")
            classrooms = ClassroomModel.objects.none()
        else:
            classrooms = ClassroomModel.objects.filter(
                academic_year=active_year, is_deleted=False
            ).select_related("academic_year")

        return render(
            request,
            self.template_name,
            {
                "classrooms": classrooms,
                "active_year": active_year,
            },
        )


class ClassroomManageStudentsView(AdminRequiredMixin, View):
    template_name = "academic/grade/classroom_manage_students.html"

    def get(self, request, class_id):
        classroom = get_object_or_404(ClassroomModel, id=class_id)

        form = ClassroomStudentForm(classroom=classroom)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "classroom": classroom,
                "students": classroom.students.all(),
            },
        )

    def post(self, request, class_id):
        classroom = get_object_or_404(ClassroomModel, id=class_id)

        form = ClassroomStudentForm(classroom, request.POST)

        if form.is_valid():
            student = form.cleaned_data["student"]
            classroom.students.add(student)

            messages.success(request, "دانش‌آموز با موفقیت به کلاس اضافه شد.")
            return redirect("academic:classroom_manage_students", class_id=classroom.id)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "classroom": classroom,
                "students": classroom.students.all(),
            },
        )


class ClassroomRemoveStudentView(AdminRequiredMixin, View):
    def post(self, request, class_id, student_id):
        classroom = get_object_or_404(ClassroomModel, id=class_id)
        student = get_object_or_404(StudentModel, id=student_id)

        if student not in classroom.students.all():
            messages.error(request, "این دانش‌آموز عضو این کلاس نیست.")
            return redirect("academic:classroom_manage_students", class_id=classroom.id)

        classroom.students.remove(student)

        messages.success(request, "دانش‌آموز از کلاس حذف شد.")
        return redirect("academic:classroom_manage_students", class_id=classroom.id)


class ClassroomDetailView(AdminRequiredMixin, View):
    template_name = "academic/grade/classroom_detail.html"

    def get(self, request, class_id):
        classroom = get_object_or_404(ClassroomModel, id=class_id)

        students = classroom.students.all()

        sessions = classroom.schedule_sessions.select_related(
            "subject", "teacher"
        ).all()

        return render(
            request,
            self.template_name,
            {
                "classroom": classroom,
                "students": students,
                "sessions": sessions,
            },
        )


class ClassroomCreateView(AdminRequiredMixin, View):
    template_name = "academic/grade/classroom_create.html"

    def get(self, request):
        active_year = get_active_year(request)

        if not active_year:
            messages.error(
                request, "برای ساخت کلاس باید یک سال تحصیلی فعال وجود داشته باشد."
            )
            return redirect("academic:classroom_list")

        form = ClassroomForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        active_year = get_active_year(request)

        if not active_year:
            messages.error(request, "سال تحصیلی فعال یافت نشد.")
            return redirect("academic:classroom_list")

        form = ClassroomForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.academic_year = active_year
            obj.save()

            messages.success(request, "کلاس با موفقیت ایجاد شد.")
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
            messages.success(request, "کلاس با موفقیت بروزرسانی شد.")
            return redirect("academic:classroom_list")

        return render(request, self.template_name, {"form": form, "obj": obj})


class ClassroomDeleteView(AdminRequiredMixin, View):
    template_name = "academic/grade/classroom_delete.html"

    def get(self, request, class_id):
        obj = get_object_or_404(ClassroomModel, id=class_id)
        return render(request, self.template_name, {"obj": obj})

    def post(self, request, class_id):
        obj = get_object_or_404(ClassroomModel, id=class_id)

        obj.is_deleted = True
        obj.save()

        messages.success(request, "کلاس با موفقیت حذف شد.")
        return redirect("academic:classroom_list")
