from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from src.jobs.models import Jobs


class JobsListView(ListView):
    queryset = Jobs.objects.published_jobs()
    template_name = 'jobs/index.html'
    paginate_by = 10


def job_detail(request, pk):
    obj = get_object_or_404(Jobs.objects.published_jobs(), pk=pk)
    return render(request, 'jobs/detail.html', {'obj': obj})
