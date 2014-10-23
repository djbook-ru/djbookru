import json
from functools import update_wrapper

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


def render_to(template, processor=None):
    def renderer(func):
        def wrapper(request, *args, **kw):
            if processor is not None:
                ctx_proc = RequestContext(request, processors=[processor])
            else:
                ctx_proc = RequestContext(request)
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], ctx_proc)
            elif isinstance(output, dict):
                return render_to_response(template, output, ctx_proc)
            return output
        return wrapper
    return renderer


def render_to_json(func):
    def wrapper(request, *args, **kwargs):
        result = func(request, *args, **kwargs)
        data = json.dumps(result, cls=DjangoJSONEncoder)
        return HttpResponse(data, mimetype="application/json")
    return update_wrapper(wrapper, func)
