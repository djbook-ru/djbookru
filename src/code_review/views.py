from ..decorators import render_to
from .forms import CommentForm, AddSnipetForm, FileFormset
from .models import Snipet, Comment, File
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import simplejson
from django.views.generic.base import View
from django.views.generic.list_detail import object_list
from django.utils.translation import ugettext_lazy as _
from tagging.models import TaggedItem, Tag
from django.db.models import F


def index(request):
    qs = Snipet.objects.all()
    tag_name = request.GET.get('tag', None)
    tag = None
    if tag_name:
        tag = get_object_or_404(Tag, name=tag_name)
        qs = TaggedItem.objects.get_by_model(qs, tag)

    extra_context = {
        'tag': tag
    }
    return object_list(request, qs, 20,
                       template_name='code_review/index.html',
                       extra_context=extra_context)


@login_required
def rate(request, pk):
    obj = get_object_or_404(Snipet, pk=pk)
    if obj.can_rate(request.user):
        Snipet.objects.filter(pk=obj.pk).update(rating=F('rating') + 1)
        obj.rated_by.add(request.user)
    return redirect(obj)


@login_required
@render_to('code_review/add.html')
def add(request):
    form = AddSnipetForm(request.user, request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        form_validated = True
    else:
        obj = Snipet()
        form_validated = False

    file_formset = FileFormset(request.POST or None, instance=obj)

    if file_formset.is_valid() and form_validated:
        if not any(f.has_changed() for f in file_formset.forms):
            form._errors['__all__'] = form.error_class([_(u'Add at least one file')])
        else:
            obj.save()
            file_formset.save()
            return redirect(obj)

    return {
        'form': form,
        'file_formset': file_formset
    }


@render_to('code_review/details.html')
def details(request, pk):
    obj = get_object_or_404(Snipet, pk=pk)
    return {
        'object': obj,
        'can_rate': obj.can_rate(request.user)
    }


class CommentsApi(View):

    def get(self, request, file_id):
        f = get_object_or_404(File, pk=file_id)
        return self.response([comment.get_json() for comment in f.comment_set.all()])

    def post(self, request, file_id):
        f = get_object_or_404(File, pk=file_id)

        if not request.user.is_authenticated():
            return HttpResponse('Authentication required', status=400)

        try:
            data = simplejson.loads(request.read())
        except simplejson.JSONDecodeError:
            return HttpResponse('JSON decode error', status=400)

        form = CommentForm(f, request.user, data)
        if form.is_valid():
            obj = form.save()
            return self.response(obj.get_json())
        else:
            return HttpResponse('Invalid data', status=400)

    def response(self, content):
        json = simplejson.dumps(content, cls=DjangoJSONEncoder)
        return HttpResponse(json, mimetype="application/json")

comments_api = CommentsApi.as_view()
