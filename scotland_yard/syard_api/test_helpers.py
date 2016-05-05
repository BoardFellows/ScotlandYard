from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from syard_api.test_factory import UserFactory, GameFactory
from syard_api.helper import (check_credentials,)


class HelperTests(APITestCase):
    """Test that you can successfully interact with the api endpoints."""

    def setUp(self):
        """Set up User Endpoint tests."""
        self.selena = UserFactory.create(
            username='seleniumk',
            password='markdown',
            email='selena@foo.com'
        )
        self.patrick = UserFactory.create(
            username='ptrompeter',
            password='beyonce',
            email='patrick@foo.com'
        )
        self.game1 = GameFactory.create(
            host=self.selena.profile,
            player_1=self.selena.profile,
            player_2=self.patrick.profile,
            winner=self.patrick,
            complete=True,
        )

    def test_token_creation(self):
        """Assert that tokens exist for users."""
        self.assertIsNotNone(Token.objects.get(user=self.patrick))
        self.assertIsNotNone(Token.objects.get(user=self.selena))

    def test_user_token(self):
        """Assert there are the same number of tokens as users."""
        token_count = Token.objects.count()
        user_count = User.objects.count()
        self.assertEqual(token_count, user_count)

    def test_credentials(self):
        p = {username: 'ptrompeter', password: 'beyonce'}
        s = {username: 'seleniumk', password: 'markdown'}
        self.assertEqual(self.patrick, check_credentials(p))
        self.assertEqual(self.selena, check_credentials(s))

    def test_credentials_fails(self):
        pass

