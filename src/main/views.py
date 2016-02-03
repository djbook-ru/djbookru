# -*- coding: utf-8 -*-

import markdown

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import translation
from django.utils.http import is_safe_url
from django.utils.translation import ugettext_lazy as _
from src.utils.urlize import urlize
from src.utils.views import object_list

from .. decorators import render_to

from . import forms
from . import models


@render_to('main/index.html')
def index(request):
    return {}


def search(request):
    q = request.GET.get('q', '')
    form = forms.SearchForm(request.GET)
    search_qs = form.search()

    extra_context = {
        'searching_for': q,
        'form': form
    }

    return object_list(request, search_qs, 30,
                       template_name='main/search.html',
                       extra_context=extra_context)


@render_to('main/feedback.html')
def feedback(request):
    if request.method == 'POST':
        form = forms.FeedbackForm(request.POST, initial={'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            form.send(request)
            messages.success(request, _(u'Feedback sent success!'))
            return redirect('main:feedback')
    else:
        form = forms.FeedbackForm(initial={'referer': request.META.get('HTTP_REFERER', '')})
    return {
        'form': form
    }


@render_to('main/thanks.html')
def thanks(request):
    return {}


def test_error_email(request):
    raise Exception('Test!')
    return


@login_required
@render_to('main/markdown_preview.html')
def markdown_preview(request):
    data = request.POST.get('data', '')
    data = urlize(markdown.markdown(data, safe_mode='escape'))
    return {'data': data}


def lang(request, lang_code):
    next = request.META.get('HTTP_REFERER')
    if not is_safe_url(url=next, host=request.get_host()):
        next = '/'
    response = HttpResponseRedirect(next)
    if lang_code and translation.check_for_language(lang_code):
        if hasattr(request, 'session'):
            request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code,
                                max_age=settings.LANGUAGE_COOKIE_AGE,
                                path=settings.LANGUAGE_COOKIE_PATH,
                                domain=settings.LANGUAGE_COOKIE_DOMAIN)
    return response
