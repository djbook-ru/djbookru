from django.forms.widgets import Input
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

class TagAutocomplete(Input):
	input_type = 'text'
	
	def render(self, name, value, attrs=None):
		json_view = reverse('tagging_autocomplete-list')
		html = super(TagAutocomplete, self).render(name, value, attrs)
		js = u'<script type="text/javascript">jQuery().ready(function() { jQuery("#%s").autocomplete("%s", { multiple: true }); });</script>' % (attrs['id'], json_view)
		return mark_safe("\n".join([html, js]))
	
	class Media:
		js_base_url = getattr(settings, 'TAGGING_AUTOCOMPLETE_JS_BASE_URL','%s/jquery-autocomplete' % settings.MEDIA_URL)
		css = {
		    'all': ('%s/jquery.autocomplete.css' % js_base_url,)
		}
		js = (
			'%s/lib/jquery.js' % js_base_url,
			'%s/jquery.autocomplete.js' % js_base_url,
			)