from django.http import HttpResponse
from poll.models import Poll, Item, Vote, Choice
from django.db import transaction
from django.contrib.auth.models import AnonymousUser
from django.utils import simplejson
from utils import set_cookie

def authpassQueue(user, queue):
    if queue != None:
        if queue.auth and not user.has_perm('Poll.can_vote'):
            return False
    return True

#TODO: Need to optimize
@transaction.commit_on_success
def poll_ajax_vote(request, poll_pk):
    if request.is_ajax():
        
        queue = Poll.publish_manager.get(pk=poll_pk).queue
        if not authpassQueue(request.user, queue):    
            return HttpResponse(status=400)
        
        try:
            chosen_items = simplejson.loads(request.GET['chosen_items'])
        except:
            return HttpResponse(status=400)
        
        poll = Poll.objects.get(pk=poll_pk)
        
        if isinstance(request.user, AnonymousUser):
            user = None
        else:
            user = request.user 
        
        vote = Vote.objects.create(poll=poll,
                                   ip=request.META['REMOTE_ADDR'],
                                   user=user)
        
        for item_pk, value in chosen_items.items():
            item = Item.objects.get(pk=item_pk)
            
            if item.userbox:
                Choice.objects.create(vote=vote, item=item, uservalue=value)
            else:
                Choice.objects.create(vote=vote, item=item)
        
        response = HttpResponse(status=200)
        set_cookie(response, poll.get_cookie_name(), poll_pk)
        
        return response
    return HttpResponse(status=400)

def poll_ajax_result(request, poll_pk):
    if request.is_ajax():
        poll = Poll.objects.get(pk=poll_pk)        
        #Send data for results
        data = {}
        
        for item in Item.objects.filter(poll=poll):
            subdata = {
                       'index': item.index,
                       'title': item.value,
                       'count': Choice.objects.filter(item=item).count(),
                       }
            
            data[item.pk] = subdata
            
        data['total'] = Vote.objects.filter(poll=poll).count()
        
        return HttpResponse(simplejson.dumps(data))
    return HttpResponse(status=400)