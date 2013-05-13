from django.template import Context
from django.template.loader import get_template
from django import template

register = template.Library()


@register.filter
def bootstrap(element, options=''):
    #deprecated
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


def bootstrap_form(element, nolabel=False, extra_class=''):
    element_type = element.__class__.__name__.lower()

    context = {
        'nolabel': nolabel
    }

    if element_type == 'boundfield':
        template = get_template("bootstrapform/field.html")
        context['field'] = element

    else:
        template = get_template("bootstrapform/form.html")
        if extra_class:
            for field in element.visible_fields():
                if not 'class' in field.field.widget.attrs:
                    field.field.widget.attrs['class'] = ''
                field.field.widget.attrs['class'] += ' %s' % extra_class
        context['form'] = element

    return template.render(Context(context))

register.simple_tag(bootstrap_form, name='bootstrap')

@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"


@register.filter
def is_radio(field):
    return field.field.widget.__class__.__name__.lower() == "radioselect"
