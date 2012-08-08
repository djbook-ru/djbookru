from django.db import models
from tagging.fields import TagField
from tagging_autocomplete.widgets import TagAutocomplete
from django.contrib.admin.widgets import AdminTextInputWidget

# The following code is based on models.py file from django-tinymce by Joost Cassee

class TagAutocompleteField(TagField):
    """
    TagField with autocomplete widget
    """
    def formfield(self, **kwargs):
        defaults = {'widget': TagAutocomplete}
        defaults.update(kwargs)

        # As an ugly hack, we override the admin widget
        if defaults['widget'] == AdminTextInputWidget:
            defaults['widget'] = TagAutocomplete

        return super(TagAutocompleteField, self).formfield(**defaults)
