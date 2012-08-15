from .forms import CommentForm
from decorators import render_to_json, render_to
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from .models import Comment
from django.db.models import Count


@csrf_exempt
@render_to_json
def load_comments(request):
    page = request.POST.get('page')
    xpath = request.POST.get('xpath')
    output = []

    if page and xpath:
        qs = Comment.objects.filter(page=page, xpath=xpath)
        for obj in qs:
            output.append({
                'content': obj.get_content(),
                'created': obj.created,
                'author': unicode(obj.author),
                'avatar': obj.author.avatar(),
                'author_url': obj.author.get_absolute_url()
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
        output = list(Comment.objects.filter(page=page).values('xpath').annotate(count=Count('id')))

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
    return {
        'isAuthenticated': request.user.is_authenticated()
    }
