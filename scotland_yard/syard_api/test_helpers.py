from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from syard_api.test_factory import UserFactory, GameFactory
from syard_api.helper import (
    check_credentials,
    get_credentials,
    get_auth_user,
    get_token_auth_user,
    get_basic_auth_user,
    get_auth_header,
)


class HelperTests(APITestCase):
    """Test that you can successfully interact with the api endpoints."""

    def setUp(self):
        """Set up User Endpoint tests."""
        self.selena = UserFactory.create(
            username='seleniumk',
            email='selena@foo.com'
        )
        self.selena.set_password('markdown')
        self.patrick = UserFactory.create(
            username='ptrompeter',
            email='patrick@foo.com'
        )
        self.patrick.set_password('beyonce')
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
        """Assert check_credentials returns authenticated user."""
        p = {'username': 'ptrompeter', 'password': 'beyonce'}
        s = {'username': 'seleniumk', 'password': 'markdown'}
        self.assertEqual(self.patrick, check_credentials(p))
        self.assertEqual(self.selena, check_credentials(s))

    def test_credentials_fails(self):
        """Assert that if credentials are not valid, check_credentials raises appropriate error."""
        p = {'username': 'ptrompeter', 'password': 'bedgsdgs'}
        s = {'username': 'agfjw;lsk', 'password': 'markdown'}
        t = {'username': 'agfjw;lsk', 'password': 'madfslkdslrkdown'}
        ex = AuthenticationFailed
        with self.assertRaises(ex):
            check_credentials(p)
        with self.assertRaises(ex):
            check_credentials(s)
        with self.assertRaises(ex):
            check_credentials(t)

    def test_get_auth_header(self):
        """Assert get_auth_header returns a list with Auth header info."""
        pass

    def test_get_auth_header_errors(self):
        """Test get_auth_header.

        Assert raises appropriate error if there is no Auth header.
        """
        pass

    def test_get_credentials(self):
        """Test get_credentials.

        Assert unencrypts basic auth and returns a dict of username and
        password.
        """
        pass

    def test_get_credentials_errors(self):
        """Test failing get_credentials.

        Assert that if basic auth header is incorrect, will raise the
        appropriate errors.
        """
        pass

    def test_get_basic_auth_user(self):
        """Test get_basic_auth_user.

        Assert that method takes an auth header with basic auth and
        returns a user object.
        """
        pass

    def test_get_basic_auth_user_fails(self):
        """Test Failing get_basic_auth_user.

        Assert that if basic auth header is incorrect,
        method will raise the appropriate errors.
        """
        pass

    def test_get_token_user(self):
        """Test get_token_user.

        Assert that method will take the tokenauth header and
        return the corresponding object.
        """
        pass

    def test_get_token_user_fails(self):
        """Test failing get_token_user.

        Assert that if tokenauth header is incorrect,
        method will raise the appropriate errors.
        """
        pass

    def test_get_auth_user_with_token(self):
        """Test get_auth_user with token auth header.

        Assert that if there are valid headers,
        method will return the corresponding user
        """
        pass

    def test_get_auth_user_with_basic(self):
        """Test get_auth_user with basic auth header.

        Assert that if there are valid headers,
        method will return the corresponding user
        """
        pass

    def test_get_auth_user_with_token_fails(self):
        """Test failing get_auth_user with token auth header.

        Assert that if there are invalid headers, method will raise error.
        """
        pass

    def test_get_auth_user_with_basic_fails(self):
        """Test failing get_auth_user with basic auth header.

        Assert that if there are invalid headers, method will raise error.
        """
        pass

    def test_get_auth_user_no_auth_header(self):
        """Test failing get_auth_user.

        Assert that if there are no auth headers, raises an error.
        """
        pass
