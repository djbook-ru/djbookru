from decorators import render_to
from main.models import Page, Book
from django.http import Http404
from django.db.models import ObjectDoesNotExist

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