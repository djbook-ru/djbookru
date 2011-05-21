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
        self.fields['category'].help_text = _(
            u'Choose the category for your recipe in which it should be placed in. '
            'If no category is matching your needs, choose any and write note to us. '
            'We will add new category as far as we can.')
        self.fields['content'].help_text = _(
            u'Use Markdown for formating the content. All HTML will be escaped.')
        self.fields['note'].help_text = _(
            u'Left the note for us. For instance, your email for this recipe, '
            'if it does not exist in your profile.')

    def save(self, user):
        obj = super(AddExampleForm, self).save(False)
        obj.approved = False
        obj.author = user
        obj.save()

        subject = _(u'New recipe has been added on djbook.ru')
        message = _(u'User %(author)s added a new recipe on djbook.ru.\n\n'
                    'Please check and approve it. URL: %(link)s') % {
            'link': 'http://%s%s' % (Site.objects.get_current().domain, obj.get_edit_url()),
            'author': obj.author}
        mail_managers(subject, message, True)
        return obj
