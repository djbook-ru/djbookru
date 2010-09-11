from decorators import render_to, render_to_json
from main.models import Page, Book
from django.http import Http404
from django.db.models import ObjectDoesNotExist
from main.forms import FeedbackForm
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

@render_to('main/index.html')
def index(request):
    try:
        book = Book.get()
        page = book.pages.get(slug='index')
    except ObjectDoesNotExist:
        page = None
    return {
        'page': page
    }

@render_to('main/page.html')    
def page(request, slug):
    try:
        book = Book.get()
        page = book.pages.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404
    return {
        'page': page
    }
    
@render_to('main/search.html')
def search(request):
    return {}

@render_to('main/feedback.html')
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, initial={'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            form.send(request)
            messages.success(request, _(u'Feedback sent success!'))
            return redirect('main:feedback')
    else:
        form = FeedbackForm(initial={'referer': request.META.get('HTTP_REFERER', '')})
    return {
        'form': form
    }