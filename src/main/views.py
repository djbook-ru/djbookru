from decorators import render_to, render_to_json
from main.models import Page, Book
from django.http import Http404
from django.db.models import ObjectDoesNotExist
from main.forms import FeedbackForm

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

@render_to_json
def feedback(request):
    output = dict(success=False)
    form = FeedbackForm(request.POST)
    if form.is_valid():
        form.send(request)
        output['success'] = True
    else:
        output['errors'] = form.get_errors()
    return output