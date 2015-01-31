import factory
from src.accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda i: 'username%s' % i)
    first_name = factory.Sequence(lambda i: 'first_name%s' % i)
    last_name = factory.Sequence(lambda i: 'last_name%s' % i)
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)
    is_valid_email = True
    password = factory.PostGenerationMethodCall('set_password',
                                                'defaultpassword')
