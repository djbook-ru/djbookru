from django import template
from poll.models import Poll, Item, Queue, Vote
from django.conf import settings
from django.utils.safestring import SafeUnicode
from django.utils.datetime_safe import datetime
from poll.ajax import authpassQueue

register = template.Library()

@register.inclusion_tag('polls.html', takes_context=True)
def poll(context, poll):
    return {'poll': poll, 'items': Item.objects.filter(poll=poll), 'user': context['user'], 'request': context['request'], 'STATIC_URL': settings.MEDIA_URL}

@register.inclusion_tag('polls.html', takes_context=True)
def poll_queue(context, queue):
    if isinstance(queue, SafeUnicode):
        tmp_queue = Queue.objects.get(title=queue)
    else:
        tmp_queue = Queue.objects.get(queue)
    
    if authpassQueue(context['user'], tmp_queue):
        tmp_polls = Poll.publish_manager.filter(queue=tmp_queue, startdate__lte=datetime.now())
        
        if len(tmp_polls) > 0:
            cur_poll = tmp_polls[0]
        else:
            cur_poll = None
        
        return poll(context, cur_poll)

class RenderItemsClass(template.Node):
    def __init__(self, poll, items):
        self.poll=template.Variable(poll)
        self.items=template.Variable(items)
        
    def render(self, context):
        poll = self.poll.resolve(context)
        items = self.items.resolve(context)
        #'name' = item.pk
        pattern1 = '{3}<br /><input name="poll_{0}" type="{1}" id="{2}" value="" /><br />'
        pattern2 = '<input name="poll_{0}" type="{1}" id="{2}" /> {3}<br />'
        result = ''
        
        #Choose an input type
        for item in items:
            if item.userbox:
                input_type = 'textbox'
                pattern = pattern1
            else:
                if poll.polltype.index == 0:
                    input_type = 'radio'
                elif poll.polltype.index == 1:
                    input_type = 'checkbox'
                pattern = pattern2
                    
            result += pattern.format(poll.pk, input_type, item.pk, item.value)
            
        return result

@register.tag
def render_items(parser, token):
    tag, poll, items = token.split_contents()
    return RenderItemsClass(poll, items)