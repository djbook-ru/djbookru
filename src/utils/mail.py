# -*- coding: utf-8 -*-

from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage


def send_templated_email(to, subject, body_template, context,
                         from_email=None, ct="html", fail_silently=False):

    if not isinstance(to, list):
        to = [to]

    context['domain'] = Site.objects.get_current().domain
    context['protocol'] = 'http'
    message = render_to_string(body_template, context)

    email = EmailMessage(subject, message, from_email, to)
    email.content_subtype = ct
    email.send(fail_silently)
