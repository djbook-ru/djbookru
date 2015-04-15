import json

from django.template import loader, RequestContext
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage
from django.template.response import TemplateResponse


# FIXME: remove this
def direct_to_template(request, template, extra_context=None, mimetype=None, **kwargs):
    """
    Render a given template with any extra URL parameters in the context as
    ``{{ params }}``.
    """
    if extra_context is None:
        extra_context = {}
    dictionary = {'params': kwargs}
    for key, value in extra_context.items():
        if callable(value):
            dictionary[key] = value()
        else:
            dictionary[key] = value
    c = RequestContext(request, dictionary)
    t = loader.get_template(template)
    return HttpResponse(t.render(c), content_type=mimetype)


# FIXME: use build in
class JsonResponse(HttpResponse):
    """
        JSON response
    """
    def __init__(self, content, mimetype='application/json', status=None):
        super(JsonResponse, self).__init__(
            content=json.dumps(content),
            content_type=mimetype,
            status=status
        )


# FIXME: Remove this
def object_list(request, queryset, paginate_by=None, page=None,
        allow_empty=True, template_name=None, template_loader=loader,
        extra_context=None, context_processors=None, template_object_name='object',
        mimetype=None):
    """
    Generic list of objects.

    Templates: ``<app_label>/<model_name>_list.html``
    Context:
        object_list
            list of objects
        is_paginated
            are the results paginated?
        results_per_page
            number of objects per page (if paginated)
        has_next
            is there a next page?
        has_previous
            is there a prev page?
        page
            the current page
        next
            the next page
        previous
            the previous page
        pages
            number of pages, total
        hits
            number of objects, total
        last_on_page
            the result number of the last of object in the
            object_list (1-indexed)
        first_on_page
            the result number of the first object in the
            object_list (1-indexed)
        page_range:
            A list of the page numbers (1-indexed).
    """
    if extra_context is None:
        extra_context = {}
    queryset = queryset._clone()
    if paginate_by:
        paginator = Paginator(queryset, paginate_by, allow_empty_first_page=allow_empty)
        if not page:
            page = request.GET.get('page', 1)
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                # Page is not 'last', nor can it be converted to an int.
                raise Http404
        try:
            page_obj = paginator.page(page_number)
        except InvalidPage:
            raise Http404
        c = {
            '%s_list' % template_object_name: page_obj.object_list,
            'paginator': paginator,
            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages(),

            # Legacy template context stuff. New templates should use page_obj
            # to access this instead.
            'results_per_page': paginator.per_page,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page': page_obj.number,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'first_on_page': page_obj.start_index(),
            'last_on_page': page_obj.end_index(),
            'pages': paginator.num_pages,
            'hits': paginator.count,
            'page_range': paginator.page_range,
        }
    else:
        c = {
            '%s_list' % template_object_name: queryset,
            'paginator': None,
            'page_obj': None,
            'is_paginated': False,
        }
        if not allow_empty and len(queryset) == 0:
            raise Http404
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    if not template_name:
        model = queryset.model
        template_name = "%s/%s_list.html" % (model._meta.app_label, model._meta.object_name.lower())
    c = RequestContext(request, c, context_processors)
    return TemplateResponse(request, template_name, c)
