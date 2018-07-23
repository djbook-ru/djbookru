# -*- coding: utf-8 -*-

from django.forms.forms import pretty_name


class PlaceholderMixin(object):

    def __init__(self, *args, **kwargs):
        super(PlaceholderMixin, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not 'placeholder' in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label or pretty_name(name)


class AjaxForm(object):

    def get_errors(self):
        from django.utils.encoding import force_unicode
        output = {}
        for key, value in self.errors.items():
            output[key] = '/n'.join([force_unicode(i) for i in value])
        return output
