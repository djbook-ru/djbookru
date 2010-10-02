# -*- coding: utf-8 -*-

from claims.models import Claims, ClaimStatus
from django.db.models import Count, Max
from django.http import HttpResponse
from datetime import datetime

def index(request):
    """ This function handles users' claims on spelling error.
    It saves all information into Claims model. It doesn't check
    the fields' length. """
    if (request.is_ajax()):
        record = Claims(ctx_left=request.POST.get('ctx_left', ''),
                        selected=request.POST.get('selected', 'None'),
                        ctx_right=request.POST.get('ctx_right', ''),
                        email=request.POST.get('email', 'unknown@hz.ru'),
                        notify='true' == request.POST.get('notify', None),
                        comment=request.POST.get('comment', 'No comments...'),
                        url=request.META.get('HTTP_REFERER', ''),
                        datetime=datetime.now())
        record.save()
        status = ClaimStatus(claim=record, status=1, applied=datetime.now())
        status.save()
        return HttpResponse('<result>ok</result>', mimetype="text/xml")
    else:
        return HttpResponse('<result>error</result>', mimetype="text/xml")

def pending(request):
    """ Функция возвращает количество жалоб в очереди. """
    if request.is_ajax():
        inner_qs = ClaimStatus.objects \
            .values('claim_id').annotate(Max('applied')) \
            .values('applied__max')

        qs = ClaimStatus.objects \
            .values('status').annotate(Count('id')) \
            .filter(applied__in=inner_qs.query) \
            .values_list('status', 'id__count')

        statuses = dict(qs)

        return HttpResponse(''.join(['<result><code>200</code><desc>success</desc>',
                                     '<pending>%i</pending>' % statuses.get('1', 0),
                                     '<assigned>%i</assigned>' % statuses.get('2', 0),
                                     '<fixed>%i</fixed>' % statuses.get('3', 0),
                                     '<invalid>%i</invalid>' % statuses.get('4', 0),
                                     '<readers>%i</readers></result>' % 1]),
                            mimetype="text/xml")
    else:
        return HttpResponse('<result><code>400</code><desc>it must be ajax call</desc></result>',
                            mimetype="text/xml")