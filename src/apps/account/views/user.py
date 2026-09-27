from django.db.models import Q
from django.views.generic import DetailView, ListView

from apps.account.enums import UserRoleEnum
from apps.account.mixins import AdminRequiredMixin
from apps.account.models import User


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "account/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        qs = User.objects.all().order_by("-created_at")

        search = self.request.GET.get("search")
        role = self.request.GET.get("role")

        if search:
            qs = qs.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(phone_number__icontains=search)
            )

        if role and role in UserRoleEnum.values:
            qs = qs.filter(role=role)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = UserRoleEnum.choices
        context["selected_role"] = self.request.GET.get("role", "")
        context["search_value"] = self.request.GET.get("search", "")
        return context


class UserDetailView(AdminRequiredMixin, DetailView):
    model = User
    template_name = "account/user_detail.html"
    context_object_name = "user"
