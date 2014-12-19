# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from .. decorators import render_to
from .models import News


class NewsListView(ListView):
    queryset = News.objects.approved()
    template_name = 'news/index.html'
    paginate_by = 10

index = NewsListView.as_view()


@render_to('news/news.html')
def news(request, pk):
    return {
        'obj': get_object_or_404(News.objects.approved(), pk=pk)
    }
