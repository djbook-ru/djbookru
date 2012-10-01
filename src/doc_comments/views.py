# -*- coding: utf-8 -*-
from . import models
from .. decorators import render_to_json
from .forms import CommentForm
from django.db.models import Count
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@render_to_json
def close_comment(request):
    id = request.POST.get('id')
    user = request.user

    if id and user.is_authenticated() and user.has_perm('doc_comments.change_comment'):
        models.Comment.objects.filter(pk=id).update(status=models.Comment.CLOSED)

    return {}


@csrf_exempt
@render_to_json
def accept_comment(request):
    id = request.POST.get('id')
    user = request.user

    if id and user.is_authenticated() and user.has_perm('doc_comments.change_comment'):
        models.Comment.objects.filter(pk=id).update(status=models.Comment.ACCEPTED)

    return {}


@csrf_exempt
@render_to_json
def load_comments(request):
    page = request.POST.get('page')
    xpath = request.POST.get('xpath')
    output = []

    if page and xpath:
        qs = models.Comment.objects.filter(page=page, xpath=xpath)
        for obj in qs:
            output.append({
                'id': obj.pk,
                'content': obj.get_content(),
                'created': obj.created,
                'author': unicode(obj.author),
                'avatar': obj.author.avatar(),
                'author_url': obj.author.get_absolute_url(),
                'status': obj.status,
                'link': obj.get_absolute_url()
            })
    return {
        'data': output
    }


@csrf_exempt
@render_to_json
def load_comments_info(request):
    page = request.POST.get('page')
    output = []

    if page:
        output = list(models.Comment.objects.filter(page=page).values('xpath').annotate(count=Count('id')))

    return {
        'data': output
    }


@csrf_exempt
@render_to_json
def add(request):
    if not request.user.is_authenticated():
        return {
            'error': ugettext(u'You are not authenticated.')
        }

    form = CommentForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        return {}
    else:
        return {
            'error': 'Form is not valid'
        }


@csrf_exempt
@render_to_json
def get_login_status(request):
    user = request.user
    return {
        'isAuthenticated': user.is_authenticated(),
        'canChangeStatus': user.is_authenticated() and user.has_perm('doc_comments.change_comment')
    }
