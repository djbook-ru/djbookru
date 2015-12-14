from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.utils.encoding import uri_to_iri

from .models import Jobs
from .forms import AddPositionForm


class JobsListView(ListView):
    queryset = Jobs.objects.published_jobs()
    template_name = 'jobs/index.html'
    paginate_by = 3


class CompanyAllVacanciesListView(ListView):
    template_name = 'jobs/list_vacancies_company.html'

    def get_queryset(self):
        # transform a URL string to a string IRI
        company = uri_to_iri(self.kwargs['company'])
        return get_list_or_404(Jobs, company_name__iexact=company)

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


@login_required
def add_position(request):
    form = AddPositionForm(request.POST or None)

    if form.is_valid():
        form.save(request.user)
        messages.success(request, _(u'The vacancy has been added successfully and will be reviewed as soon as possible.'))
        return redirect(reverse('jobs:index'))

    return render(request, 'jobs/add.html', {'form': form})


def edit_position(request, pk):
    # function for edit vacancy
    resp = u'Soon...'
    return HttpResponse(resp)
