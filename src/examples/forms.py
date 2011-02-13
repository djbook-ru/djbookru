from django import forms
from examples.models import Example
from django.core.mail import mail_managers
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

class AddExampleForm(forms.ModelForm):
    
    class Meta:
        model = Example
        fields = ('title', 'category', 'content', 'note')
        
    def save(self, user):
        obj = super(AddExampleForm, self).save(False)
        obj.approved = False
        obj.author = user
        obj.save()
        
        subject = _(u'New recipe was added on djbook.ru by user: %(author)s') % {'author': obj.author} 
        message = _(u'New recipe was added on djbook.ru. Check please and approve it. %(link)s') % {
                'link': 'http://%s%s' % (Site.objects.get_current().domain, obj.get_edit_url())
            }
        mail_managers(subject, message, True)
        return obj