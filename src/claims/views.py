# -*- coding: utf-8 -*-

from claims.models import Claims, ClaimStatus
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
                        notify='true'==request.POST.get('notify', None),
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
        return HttpResponse(''.join(['<result><code>200</code><desc>success</desc>',
                                     '<pending>%i</pending>' % get_claims_count_by_status(1),
                                     '<assigned>%i</assigned>' % get_claims_count_by_status(2),
                                     '<fixed>%i</fixed>' % get_claims_count_by_status(3),
                                     '<invalid>%i</invalid>' % get_claims_count_by_status(4),
                                     '<readers>%i</readers></result>' % 1]),
                            mimetype="text/xml")
    else:
        return HttpResponse('<result><code>400</code><desc>it must be ajax call</desc></result>',
                            mimetype="text/xml")

def get_claims_count_by_status(code):
    from django.db import connection
    cursor = connection.cursor()
    sql = ' '.join(['select count(*) from claims_claimstatus',
                    'where status=%i and applied in',
                    '(select max(applied) from claims_claimstatus',
                    'group by claim_id)'])
    cursor.execute(sql % code)

    return cursor.fetchone()[0]