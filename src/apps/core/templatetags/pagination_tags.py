from django import template


register = template.Library()


@register.simple_tag
def pagination_url(request, page_number):
    query_params = request.GET.copy()

    query_params.pop("page", None)

    query_params["page"] = page_number

    return query_params.urlencode()
