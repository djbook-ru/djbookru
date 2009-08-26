# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

from django.template import RequestContext

def render_to(template, processor):
    if not callable(processor):
        raise Exception('Processor is not callable.')
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request, processors=[processor]))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request, processors=[processor]))
            return output
        return wrapper
    return renderer

