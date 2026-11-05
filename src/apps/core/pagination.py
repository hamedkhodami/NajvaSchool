from django.core.paginator import Paginator
from django.views.generic import ListView


class BasePaginatedListView(ListView):
    paginate_by = 10


def paginate_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)

    page_obj = paginator.get_page(request.GET.get("page"))

    return {
        "paginator": paginator,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "object_list": page_obj.object_list,
    }
