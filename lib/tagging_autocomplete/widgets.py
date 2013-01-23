from django.forms.widgets import Input
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe


class TagAutocomplete(Input):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        json_view = reverse('tagging_autocomplete-list')
        html = super(TagAutocomplete, self).render(name, value, attrs)
        js = u'<script type="text/javascript">jQuery(function($) { $("#%s").autocomplete("%s", { multiple: true }); });</script>' % (attrs['id'], json_view)
        return mark_safe("\n".join([html, js]))

    class Media:
        css = {
            'all': ('jquery-autocomplete/jquery.autocomplete.css',)
        }
        js = (
            'js/force_jquery.js',
            'jquery-autocomplete/jquery.autocomplete.js',
        )
