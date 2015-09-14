from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from src.jobs.models import Jobs


class JobsListView(ListView):
    queryset = Jobs.objects.published_jobs()
    template_name = 'jobs/index.html'
    paginate_by = 3


class CompanyAllVacanciesListView(ListView):
    template_name = 'jobs/list_vacancies_company.html'

    def get_queryset(self):
        return get_list_or_404(Jobs, company_name__iexact=self.kwargs['company'])

    def get_context_data(self, **kwargs):
        context = super(CompanyAllVacanciesListView, self).get_context_data(**kwargs)
        # getting company name
        context['company'] = self.object_list[0].company_name
        # get a number of positions in the company
        context['num_of_vac'] = len(self.object_list)
        return context


class JobDetailView(DetailView):
	model = Jobs
	template_name = 'jobs/detail.html'

	def get_context_data(self, **kwargs):
		context = super(JobDetailView, self).get_context_data(**kwargs)
		# learn the number of vacancies of this company
		context['num_of_vac'] = len(get_list_or_404(Jobs,
			                        company_name__iexact=self.object.company_name))
		return context


def vacancy_edit(request, pk):
    # function for edit vacancy
    resp = u'Soon...'
    return HttpResponse(resp)
