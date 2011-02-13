from django import forms
from examples.models import Example
from django.core.mail import mail_managers
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.utils.html import escape

class AddExampleForm(forms.ModelForm):
    
    class Meta:
        model = Example
        fields = ('title', 'category', 'content', 'note')
    
    def __init__(self, *args, **kwargs):
        super(AddExampleForm, self).__init__(*args, **kwargs)
        self.fields['category'].help_text = _(u'''Chose category you think your example should be placed in. 
If this one does not exist - chose any and write in Note. We will add later.''')
        self.fields['content'].help_text = _(u'Use Markdown for formating. All HTML will be escaped.')
        self.fields['note'].help_text = _(u'Left some note. Your email for example, if it does not exist in profile.')
        
    def save(self, user):
        obj = super(AddExampleForm, self).save(False)
        obj.content = escape(obj.content)
        obj.approved = False
        obj.author = user
        obj.save()
        
        subject = _(u'New recipe was added on djbook.ru by user: %(author)s') % {'author': obj.author} 
        message = _(u'New recipe was added on djbook.ru. Check please and approve it. %(link)s') % {
                'link': 'http://%s%s' % (Site.objects.get_current().domain, obj.get_edit_url())
            }
        mail_managers(subject, message, True)
        return obj