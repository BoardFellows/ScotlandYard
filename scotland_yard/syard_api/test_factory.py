import factory
from django.conf import settings
from syard_main.models import Game


class UserFactory(factory.django.DjangoModelFactory):
    """Create Test User Factory."""

    class Meta():
        """Model is User."""

        model = settings.AUTH_USER_MODEL


class GameFactory(factory.django.DjangoModelFactory):
    """Create Test Game Factory."""

    class Meta():
        """Model is Game."""

        model = Game
