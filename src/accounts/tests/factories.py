import factory
from accounts.models import User


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda i: 'username%s' % i)
    first_name = factory.Sequence(lambda i: 'first_name%s' % i)
    last_name = factory.Sequence(lambda i: 'last_name%s' % i)
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)
    is_valid_email = True

    @factory.post_generation()
    def password(self, create, extracted, **kwargs):
        self.set_password(extracted)
        if create:
            self.save()
