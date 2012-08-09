from django.core.exceptions import ObjectDoesNotExist
from social_auth.backends.exceptions import AuthException, StopPipeline
from social_auth.models import UserSocialAuth
from django.utils.translation import ugettext_lazy as _


def create_user(backend, details, response, uid, username, user=None, *args,
                **kwargs):
    """Create user. Depends on get_username pipeline."""
    if user:
        return {'user': user}
    if not username:
        return None

    email = details.get('email') or None

    try:
        UserSocialAuth.get_user_by_email(email=email)
        raise AuthException(backend, _('This email is already used by other account. If it is your account, login and connect it on profile edit page.'))
    except ObjectDoesNotExist:
        pass

    return {
        'user': UserSocialAuth.create_user(username=username, email=email),
        'is_new': True
    }
