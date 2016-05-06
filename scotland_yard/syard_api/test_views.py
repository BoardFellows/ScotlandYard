from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
<<<<<<< HEAD
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
        self.frasier = UserFactory.create()
        self.game1 = GameFactory.create(
            host=self.selena.profile,
            player_1=self.selena.profile,
            player_2=self.patrick.profile,
            winner=self.patrick,
            complete=True,

        )
        self.game2 = GameFactory.create(
            host=self.frasier,
            player_1=self.frasier,
            player_2=self.patrick.profile,
        )

    def test_post_users_list(self):
        """Assert that POST /users/ creates a new user."""
        self.assertEqual(User.objects.count(), 2)
        url = '/users/'
        data = {'username': 'Phil', 'email': 'test@foo.com', 'password': 'something'}
        client = APIClient(enforce_csrf_checks=True)
        request = client.post(url, data, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_get_board(self):
        """Assert that GET /board returns a JSON representation of the board."""
        pass

    def test_get_users_list(self):
        """Assert that GET /users/ with works with basic auth."""
        pass

    def test_get_users_list_fails(self):
        """Assert that GET /users/ fails without basic auth."""
        pass

    def test_get_user_detail(self):
        """Assert that GET /users/:id is successful with token auth."""
        pass

    def test_get_user_detail_fails(self):
        """Assert that GET /users/:id is fails without token auth."""
        pass

    def test_get_games(self):
        """Assert that GET /games/ returns all user's games."""
        pass

    def test_get_games_fails(self):
        """Assert that GET /games/ does not return other user's games."""
        pass

    def test_post_games(self):
        """Assert that POST /games/ creates a new game if authenticated."""
        pass

    def test_post_games_fails(self):
        """Assert that POST /games/ fails if not authenticated."""
        pass

    def test_get_game_detail(self):
        """Assert that GET /games/:id returns game information."""
        pass

    def test_update_game_state(self):
        """Assert that PUT /games/:id updates moves/returns games state."""
        pass
