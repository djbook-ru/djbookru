# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from .. decorators import render_to
from . import forms
from . import models


@login_required
def post(request):
    output = dict(success=False)
    form = forms.CommentForm(None, request.POST)
    if form.is_valid():
        form.save(request.user)
        output['success'] = True
    else:
        output['errors'] = form.get_errors()
    return HttpResponse(json.dumps(output), "text/javascript")


@render_to('comments/update_comments.html')
def update_comments(request):
    last_comment_id = request.POST.get('last_comment_id')
    object_pk = request.POST.get('obj_id')
    ct = request.POST.get('ct')
    if object_pk and ct:
        qs = models.Comment.objects.filter(content_type__pk=ct, object_pk=object_pk)
        if last_comment_id:
            try:
                last_comment = models.Comment.objects.get(pk=last_comment_id)
                qs = qs.filter(submit_date__gt=last_comment.submit_date)
            except models.Comment.DoesNotExist:
                pass
    else:
        qs = models.Comment.objects.none()
    return {
        'qs': qs
    }
