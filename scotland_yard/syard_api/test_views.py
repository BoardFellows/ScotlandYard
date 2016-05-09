from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from syard_api.test_factory import UserFactory, GameFactory
from syard_main.models import Round
from syard_main.board import BOARD
from rest_framework.test import force_authenticate
import json


class EndPointTests(APITestCase):
    """Test that you can successfully interact with the api endpoints."""

    def setUp(self):
        """Set up User Endpoint tests."""
        self.selena = UserFactory.create(
            username='seleniumk',
            email='s@foo.com'
        )
        self.selena.set_password('markdown')
        self.patrick = UserFactory.create(
            username='ptrompeter',
            email='p@foo.com'
        )
        self.patrick.set_password('beyonce')
        self.frasier = UserFactory.create(
            username='frasier',
            email='f@foo.com'

        )
        self.frasier.set_password('tswift')
        self.game1 = GameFactory.create(
            host=self.selena.profile,
            player_1=self.selena.profile,
            player_2=self.patrick.profile,
            winner=self.patrick,
            complete=True,

        )
        self.game2 = GameFactory.create(
            host=self.frasier.profile,
            player_1=self.frasier.profile,
            player_2=self.patrick.profile,
        )
        self.client = APIClient(enforce_csrf_checks=True)

    # erroring. I don't know why. Throws a key error on password.
    def test_post_users_list(self):
        """Assert that POST /users/ creates a new user."""
        self.assertEqual(User.objects.count(), 3)
        url = '/users/'
        data = {'username': 'Phil', 'email': 'test@foo.com', 'password': 'something'}
        request = self.client.post(url, data, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)

    def test_get_board(self):
        """Assert that GET /board returns a JSON representation of the board."""
        request = self.client.get('/board')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.content, str.encode(json.dumps(BOARD)))


# haven't figured out how to verify auth
    # def test_get_users_list(self):
        # """Assert that GET /users/ with works with basic auth."""
        # self.client.credentials(HTTP_AUTHORIZATION="Basic cHRyb21wZXRlcjpiZXlvbmNl")
        # self.client.force_authenticate(user=User.objects.get(username="ptrompeter"))
        # request = self.client.get('/users/')
        # self.assertEqual(request.status_code, status.HTTP_200_OK)


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
