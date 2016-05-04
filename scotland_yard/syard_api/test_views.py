from syard_main.models import UserProfile, Game
import factory
from rest_framework.authtoken.models import Token
# from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from django.conf import settings
from django.contrib.auth.models import User
import json


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


class EndPointTests(APITestCase):
    """Test that you can successfully interact with the api endpoints."""

    def setUp(self):
        """Set up User Endpoint tests."""
        self.selena = UserFactory.create(
            username='seleniumk',
            email='test@foo.com'
        )
        self.patrick = UserFactory.create(
            username='ptrompeter',
            email='test@foo.com'
        )
        self.expected_user_keys = ['id', 'username', 'email', 'password', 'profile']
        self.game1 = GameFactory.create(
            host=self.selena.profile,
            winner=self.patrick,
            complete=True,

        )

    def test_get_users_list(self):
        """Assert that the user endpoint responds to a get request."""
        url = '/users/'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(self.selena.username, request.data[0].get('username'))
        self.assertEqual(self.patrick.username, request.data[1].get('username'))
        self.assertEqual(self.expected_user_keys, list(request.data[0].keys()))

    def test_get_user_detail(self):
        """Assert that user detail endpoint contains necessary info."""
        url = '/users/' + str(self.selena.id) + '/'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(self.expected_user_keys, list(request.data.keys()))
        self.assertEqual(self.selena.id, request.data.get('id'))
        self.assertEqual(self.selena.username, request.data.get('username'))
        self.assertEqual(self.selena.email, request.data.get('email'))

    def test_post_user_detail(self):
        """Assert that new users can be added using post method."""
        self.assertEqual(User.objects.count(), 2)
        url = '/users/'
        data = {'username': 'Phil', 'email': 'test@foo.com', 'password': 'something'}
        client = APIClient(enforce_csrf_checks=True)
        request = client.post(url, data, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_get_game_list(self):
        url = '/games/'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
