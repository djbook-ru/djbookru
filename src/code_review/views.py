from ..decorators import render_to
from .forms import CommentForm
from .models import Snipet, Comment, File
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.views.generic.base import View
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required


def index(request):
    qs = Snipet.objects.all()
    extra_context = {}
    return object_list(request, qs, 20,
                       template_name='code_review/index.html',
                       extra_context=extra_context)


@render_to('code_review/details.html')
def details(request, pk):
    obj = get_object_or_404(Snipet, pk=pk)
    return {
        'object': obj
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
