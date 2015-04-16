# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from social.exceptions import AuthException


def check_email(backend, details, user=None, *args, **kwargs):
    """
    Create user. Depends on get_username pipeline.
    This pipeline rise exception if some use has same email.
    So if someone know you email on djbook.ru, he can't use it to create account
    on services supported for login and login on djbook to your account.
    Really I think it is impossible register somewhere with other one email,
    but it works as we like.
    """
    if user:
        return {}

    email = details.get('email')

    if email:
        users = list(backend.strategy.storage.user.get_users_by_email(email))
        if users:
            msg = _('"%(email)s" is already used by other account. If it is your account, '
                    'login and connect it on profile edit page.') % {'email': email}
            raise AuthException(backend, msg)
    else:
        raise AuthException(
            backend, _('Social service does not return email. Use registration form.'))

    return {}
