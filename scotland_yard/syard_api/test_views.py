from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from syard_api.test_factory import UserFactory, GameFactory


# class EndPointTests(APITestCase):
#     """Test that you can successfully interact with the api endpoints."""

#     def setUp(self):
#         """Set up User Endpoint tests."""
#         self.selena = UserFactory.create(
#             username='seleniumk',
#             email='test@foo.com'
#         )
#         self.patrick = UserFactory.create(
#             username='ptrompeter',
#             email='test@foo.com'
#         )
#         self.expected_user_keys = ['id', 'username', 'email', 'password', 'profile']
#         self.game1 = GameFactory.create(
#             host=self.selena.profile,
#             winner=self.patrick,
#             complete=True,

#         )
