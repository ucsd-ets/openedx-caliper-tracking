import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory

USER_PASSWORD = 'TEST_PASSOWRD'


class UserFactory(DjangoModelFactory):
    """
    Crete user with the given credentials.
    """
    class Meta(object):
        model = User
        django_get_or_create = ('email', 'username')

    username = factory.Sequence(u'robot{0}'.format)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.PostGenerationMethodCall('set_password', USER_PASSWORD)
    is_active = True
    is_superuser = False
