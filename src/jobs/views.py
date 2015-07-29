from django.shortcuts import render

from .models import Jobs


def index(request):
    obj = Jobs.objects.published_jobs()
    return render(request, 'jobs/index.html', {'objects': obj})
