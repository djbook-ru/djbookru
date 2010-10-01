from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import Context , loader
from django.template import RequestContext
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.syndication.feeds import Feed
from accounts.models import User
from django.contrib.auth.models import Group
from django.conf import settings
from django.views.generic.list_detail import object_list
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from  datetime  import datetime, timedelta
import simplejson

from dinette.models import Ftopics , SuperCategory ,Category ,Reply
from dinette.forms import  FtopicForm , ReplyForm

json_mimetype = 'application/javascript'
def index_page(request):
    forums = SuperCategory.objects.all()
    accesslist = ""
    jumpflag = False
    
    
    #groups which this user has access
    if request.user.is_authenticated() :
            
            groups = [group for group in request.user.groups.all()] + [group for group in Group.objects.filter(name="general")]
    else:
            #we are treating user who have not loggedin belongs to general group
            groups = Group.objects.filter(name="general")
        
    
    #logic which decide which forum does this user have access to
    for forum in forums :
        jumpflag = False
        for group in groups :           
            for gforum in group.can_access_forums.all() :
                
                if gforum.id == forum.id :
                    #the respective user can access the forum
                    #accesslist.append(True)
                    accesslist = "1"+accesslist
                    jumpflag = True
                    break
        
          #already one group has acces to forum no need to check whether other groups have access to it or not        
            if jumpflag:
                break
        
        if jumpflag == False:
            accesslist = "0"+accesslist
   
    totaltopics = Ftopics.objects.count()
    totalposts = totaltopics + Reply.objects.count()
    totalusers =  User.objects.count()
    now = datetime.now()
    users_online = User.objects.filter(last_activity__gte =  now - timedelta(seconds = 900)).count() + 1#The current user is always online. :)
    last_registered_user = User.objects.order_by('-date_joined')[0]
    try:
        user_access_list = int(accesslist)
    except ValueError:
        user_access_list = 0
    payload = {'users_online':users_online, 'forums_list':forums,'totaltopics':totaltopics,
               'totalposts':totalposts,'totalusers':totalusers,'user_access_list':user_access_list,
               'last_registered_user':last_registered_user}
    return render_to_response("dinette/mainindex.html", payload,RequestContext(request))

def category_details(request, categoryslug,  pageno=1) :
    #build a form for posting topics
    topicform = FtopicForm()
    category = get_object_or_404(Category, slug=categoryslug)
    queryset = Ftopics.objects.filter(category__id__exact = category.id)
    topiclist = queryset    
    topic_page_size = getattr(settings , "TOPIC_PAGE_SIZE", 10)
    payload = {'topicform': topicform,'category':category,'authenticated':request.user.is_authenticated(),'topic_list':topiclist, "topic_page_size": topic_page_size}
    return render_to_response("dinette/category_details.html", payload, RequestContext(request))
    
def topic_detail(request, categoryslug, topic_slug , pageno = 1):
    topic = get_object_or_404(Ftopics, slug = topic_slug)
    show_moderation_items = False
    if request.user in topic.category.moderated_by.all():
        show_moderation_items = True
    #some body has viewed this topic
    topic.viewcount = topic.viewcount + 1
    topic.save()
    #we also need to display the reply form
    replylist = topic.reply_set.all()
    reply_page_size = getattr(settings , "REPLY_PAGE_SIZE", 10)
    replyform = ReplyForm()
    payload = {'topic': topic, 'replyform':replyform,'reply_list':replylist, 'show_moderation_items':show_moderation_items, "reply_page_size": reply_page_size}
    return render_to_response("dinette/topic_detail.html", payload, RequestContext(request))

@login_required
def postTopic(request) :
    
    topic = FtopicForm(request.POST,request.FILES)
   
    if topic.is_valid() == False :
        d = {"is_valid":"false","response_html":topic.as_table()}
        json = simplejson.dumps(d)
        if request.FILES :
            json = "<textarea>"+simplejson.dumps(d)+"</textarea>"
        else:
            json = simplejson.dumps(d)
        return HttpResponse(json, mimetype = json_mimetype)                    
     
    #code which checks for flood control
    last_posttime = request.user.last_posttime
    if last_posttime and (datetime.now() - last_posttime).seconds <= settings.FLOOD_TIME:
    #oh....... user trying to flood us Stop him
        d2 = {"is_valid":"flood","errormessage":"Flood control.................."}
        if request.FILES : 
            json = "<textarea>"+simplejson.dumps(d2)+"</textarea>"
        else :
            json = simplejson.dumps(d2)  
        return HttpResponse(json, mimetype = json_mimetype)
         
    ftopic = topic.save(commit=False)     
    #only if there is any file
    if request.FILES :
        if(request.FILES['file'].content_type.find("image") >= 0 ) :
            ftopic.attachment_type = "image"
        else :
            ftopic.attachment_type = "text"
        ftopic.filename = request.FILES['file'].name
        
    ftopic.posted_by = request.user
    ftopic.category  = Category.objects.get(pk = request.POST['categoryid'])
    #Assigning user rank
    assignUserElements(request.user)
    ftopic.save()
    payload = {'topic':ftopic}
    response_html = render_to_string('dinette/topic_detail_frag.html', payload,RequestContext(request))
  
    d2 = {"is_valid":"true","response_html":response_html}
    #this the required for ajax file uploads
    if request.FILES : 
        json = "<textarea>"+simplejson.dumps(d2)+"</textarea>"
    else :
        json = simplejson.dumps(d2) 
    return HttpResponse(json, mimetype = json_mimetype)
    
@login_required    
def postReply(request) :
    freply = ReplyForm(request.POST,request.FILES)
    
    if freply.is_valid() == False :
        d = {"is_valid":"false","response_html":freply.as_table()}
        json = simplejson.dumps(d)
        if request.FILES :
            json = "<textarea>"+simplejson.dumps(d)+"</textarea>"
        else:
            json = simplejson.dumps(d)
        return HttpResponse(json, mimetype = json_mimetype)
        
        
        
    #code which checks for flood control
    last_posttime = request.user.last_posttime
    if last_posttime and (datetime.now() - last_posttime).seconds <= settings.FLOOD_TIME:
    #oh....... user trying to flood us Stop him
        d2 = {"is_valid":"flood","errormessage": _("You have posted message too recently. Please wait a while before trying again.")}
        if request.FILES : 
            json = "<textarea>"+simplejson.dumps(d2)+"</textarea>"
        else :
            json = simplejson.dumps(d2)  
        return HttpResponse(json, mimetype = json_mimetype)        
        
    
    reply = freply.save(commit=False)    
     #only if there is any file
    if len(request.FILES.keys()) == 1 :
        if(request.FILES['file'].content_type.find("image") >= 0 ) :
            reply.attachment_type = "image"
        else :
            reply.attachment_type = "text"
            
        reply.filename = request.FILES['file'].name
        
    reply.posted_by = request.user
    reply.topic = Ftopics.objects.get(pk = request.POST['topicid'])
    #Assigning user rank
    assignUserElements(request.user) 
    reply.save()
    payload = {'reply':reply}    
    response_html = render_to_string('dinette/replydetail_frag.html', payload ,RequestContext(request))
    
    d2 = {"is_valid":"true","response_html":response_html}
        
    if request.FILES :
        #this the required for ajax file uploads
        json = "<textarea>"+simplejson.dumps(d2)+"</textarea>"
    else:
        json = simplejson.dumps(d2)
    
    return HttpResponse(json, mimetype = json_mimetype)  
    
    
    
class LatestTopicsByCategory(Feed):
    title_template = 'dinette/feeds/title.html'
    description_template = 'dinette/feeds/description.html'
    
    def get_object(self, whichcategory):
        return get_object_or_404(Category, slug=whichcategory[0])
    
    def title(self, obj):
        return _("Latest topics in category %(name)s") % dict(name=obj.name)
    
    def link(self, obj):
        return  settings.SITE_URL
    
    def items(self, obj):
        return obj.ftopics_set.all()[:10]
    
    #construct these links by means of reverse lookup  by
    #using permalink decorator
    def item_link(self,obj):
        return  obj.get_absolute_url()
    
    def item_pubdate(self,obj):
        return obj.created_on
    
    
class LatestRepliesOfTopic(Feed):
    title_template = 'dinette/feeds/title.html'
    description_template = 'dinette/feeds/description.html'

    def get_object(self, whichtopic):
        return get_object_or_404(Ftopics, slug=whichtopic[0])
         
    def title(self, obj):
        return "Latest replies in topic %(subject)s" % dict(subject=obj.subject)
     
    def link(self, obj):
        return  settings.SITE_URL

    def items(self, obj):
        list = []
        list.insert(0,obj)
        for obj in obj.reply_set.all()[:10] :
            list.append(obj)           
        return list
       
     #construct these links by means of reverse lookup  by
     #using permalink decorator
    def item_link(self,obj):       
        return  obj.get_absolute_url()
     
    def item_pubdate(self,obj):
        return obj.created_on
    
    
    
def assignUserElements(user):
    totalposts = user.ftopics_set.count() + user.reply_set.count()
    user.posts_count = totalposts
    user.last_posttime = datetime.now()
    user.save()        
    
###Moderation views###
@login_required
def moderate_topic(request, topic_id, action):
    topic = get_object_or_404(Ftopics, pk = topic_id)
    if not request.user in topic.category.moderated_by.all():
        raise Http404
    if request.method == 'POST':
        if action == 'close':
            if topic.is_closed:
                message = _('You have reopened topic %(subject)s') % dict(subject=topic.subject)
            else:
                message = _('You have closed topic %(subject)s') % dict(subject=topic.subject)
            topic.is_closed = not topic.is_closed
        elif action == 'announce':
            if topic.announcement_flag:
                message = _('%(subject)s is no longer an announcement.') % dict(subject=topic.subject)
            else:
                message = _('%(subject)s is now an announcement.') % dict(subject=topic.subject)
            topic.announcement_flag = not topic.announcement_flag
        elif action == 'sticky':
            if topic.is_sticky:
                message = _('%(subject)s has been unstickied.') % dict(subject=topic.subject)
            else:
                message = _('%(subject)s has been stickied.') % dict(subject=topic.subject)
            topic.is_sticky = not topic.is_sticky
        elif action == 'hide':
            if topic.is_hidden:
                message = _('%(subject)s has been unhidden.') % dict(subject=topic.subject)
            else:
                message = _("%(subject)s has been hidden and won't show up any further.") % dict(subject=topic.subject)
            topic.is_hidden = not topic.is_hidden
        topic.save()
        payload = {'topic_id':topic.pk, 'message':message}
        resp = simplejson.dumps(payload)
        return HttpResponse(resp, mimetype = json_mimetype)
    else:
        return HttpResponse(_('This view must be called via post'))
    
def login(request):
    if getattr(settings, 'DINETTE_LOGIN_TEMPLATE', None):
        return render_to_response(settings.DINETTE_LOGIN_TEMPLATE, {}, RequestContext(request, {'fb_api_key':settings.FACEBOOK_API_KEY,}))
    else:
        from django.contrib.auth.views import login
        return login(request)
        
def user_profile(request, user_name):
    user_profile =get_object_or_404(User, username = user_name)
    return render_to_response('dinette/user_profile.html', {}, RequestContext(request, {'user_profile': user_profile}))

@login_required
def new_topics(request):
    user= request.user
    new_topic_list = user.get_since_last_visit()
    return topic_list(request, new_topic_list, page_message = _("Topics since your last visit"))
    
def active(request):
    #Time filter = 48 hours
    days_ago_2 = datetime.now() - timedelta(days = 2)
    topics = Ftopics.objects.filter(last_reply_on__gt =  days_ago_2)
    active_topics = topics.extra(select= {"activity":"viewcount+100*num_replies"}).order_by("-activity")
    return topic_list(request, active_topics, page_message = _("Most active Topics"))
    
def topic_list(request, queryset, page_message):
    payload = {"new_topic_list": queryset, "page_message": page_message}
    return render_to_response("dinette/new_topics.html", payload, RequestContext(request))

def search(request):
    return HttpResponse('TODO')
    #from haystack.views import SearchView
    #search_view = SearchView(template = "dinette/search.html")
    #return search_view(request)
    
    
    
    
    
    
    
    
    
    
    
    
    