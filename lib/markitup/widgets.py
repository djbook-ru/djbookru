from django import forms
from django.utils.safestring import mark_safe
#from django.utils import simplejson as json


class MarkItUp(forms.Textarea):
    def render(self, name, value, attrs=None):
        html = super(MarkItUp, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs, name=name)
        init_js = u"""
        <script type="text/javascript" >
            jQuery(document).ready(function($){
                $("#%(id)s").markItUp(MarkItUpSettings);
            });
        </script>
        """ % {
            'id': final_attrs.get('id'),
        }
        return mark_safe(u''.join([html, init_js]))

    class Media:
        js = (
            'markitup/django_jquery.js',
            'markitup/sets/markdown_without_priview/set.js',
            'markitup/jquery.markitup.js',
        )
        css = {'all': (
            'markitup/skins/simple/style.css',
            'markitup/sets/markdown_without_priview/style.css'
        )}
