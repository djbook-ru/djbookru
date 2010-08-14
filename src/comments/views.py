from forms import CommentForm
from django.http import HttpResponse
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from models import Comment
from django.shortcuts import render_to_response

@login_required
def post(request):
    output = dict(success=False)
    form = CommentForm(None, request.POST)
    if form.is_valid():
        form.save(request.user)
        output['success'] = True
    else:
        output['errors'] = form.get_errors()
    return HttpResponse(json.dumps(output), "text/javascript")

def update_comments(request):
    last_comment_id = request.POST.get('last_comment_id')
    object_pk = request.POST.get('obj_id')
    ct = request.POST.get('ct')
    if object_pk and ct:
        qs = Comment.objects.filter(content_type__pk=ct, object_pk=object_pk)
        if last_comment_id:
            try:
                last_comment = Comment.objects.get(pk=last_comment_id)
                qs = qs.filter(submit_date__gt=last_comment.submit_date)
            except Comment.DoesNotExist:
                pass        
    else:
        qs = Comment.objects.none()
    return render_to_response('comments/update_comments.html',{
            'qs': qs
        })