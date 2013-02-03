from django.template import Context
from django.template.loader import get_template
from django import template

register = template.Library()


@register.filter
def bootstrap(element, options=''):
    element_type = element.__class__.__name__.lower()

    if options == 'nolabel':
        nolabel = True
    else:
        nolabel = False

    if element_type == 'boundfield':
        template = get_template("bootstrapform/field.html")
        context = Context({'field': element, 'nolabel': nolabel})
    else:
        template = get_template("bootstrapform/form.html")
        context = Context({'form': element, 'nolabel': nolabel})

    return template.render(context)


@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"


@register.filter
def is_radio(field):
    return field.field.widget.__class__.__name__.lower() == "radioselect"
