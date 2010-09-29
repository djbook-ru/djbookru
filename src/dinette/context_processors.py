from dinette.models import Ftopics, SiteConfig, NavLink

def get_announcement(request):
    try:
        ancount =  Ftopics.objects.filter(announcement_flag = True).count()       
        if(ancount > 0 ) :
            announcement = Ftopics.objects.filter(announcement_flag = True).latest()
            return {'announcement': announcement,'ancount':ancount}
        
        return {'ancount':ancount}
    
    except Ftopics.DoesNotExist:
        return {}
    
def get_forumwide_links(request):
    try:
        return {"dinette_nav_links":NavLink.objects.all()}
    except:
        return {}
    
