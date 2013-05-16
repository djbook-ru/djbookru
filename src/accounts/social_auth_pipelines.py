# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from social_auth.exceptions import AuthException
from social_auth.models import UserSocialAuth


def create_user(backend, details, response, uid, username, user=None, *args,
                **kwargs):
    """
        Create user. Depends on get_username pipeline.
        This pipeline rise exception if some use has same email.
        So if someone know you email on djbook.ru, he can't use it to create account
        on services supported for login and login on djbook to your account.
        Really I think it is impossible register somewhere with other one email,
        but it works as we like.
    """
    if user:
        return {'user': user}
    if not username:
        return None

    email = details.get('email')

    try:
        UserSocialAuth.get_user_by_email(email=email)
        raise AuthException(backend, _('"%(email)s" is already used by other account. If it is your account, login and connect it on profile edit page.') % {
            'email': email
        })
    except ObjectDoesNotExist:
        pass

    user = UserSocialAuth.create_user(username=username, email=email, force_email_valid=True)

    return {
        'user': user,
        'is_new': True
    }
