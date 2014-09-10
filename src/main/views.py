# -*- coding: utf-8 -*-

import markdown

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView
from django.views.generic.list_detail import object_list
from src.forum.util import urlize

from .. decorators import render_to

from . import forms
from . import models


@render_to('main/index.html')
def index(request):
    return dict(book=models.Book.get())


@render_to('main/first_page.html')
def first_page(request):
    try:
        page = models.Book.get().pages.get(slug='index')
    except ObjectDoesNotExist:
        page = None
    return dict(page=page)


@render_to('main/page.html')
def page(request, slug):
    try:
        page = models.Book.get().pages.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404
    return dict(page=page)


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


def lang(request, code):
    next = request.META.get('HTTP_REFERER', '/')
    response = HttpResponseRedirect(next)
    if code and translation.check_for_language(code):
        if hasattr(request, 'session'):
            request.session['django_language'] = code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, code)
        translation.activate(code)
    return response


class BookRedirectView(RedirectView):
    url = '/%(slug)s.html'

book_redirect = BookRedirectView.as_view()
