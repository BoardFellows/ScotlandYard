from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase

import factory

from syard_main.models import Detective, Game, MrX, Round, UserProfile

"""Test UserProfile model."""


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game


class RoundFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Round


class MrXFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MrX


class DetectiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Detective


class UnsavedUserCase(TestCase):
    """Test if Game is not saved to database."""
    def setUp(self):
        self.user_0 = UserFactory.build(
            username='jim',
            email='jim@example.com'
        )
        self.user_0.set_password('secret')

    def test_unsaved_user(self):
        """Unsaved user should not have a user id."""
        self.assertIsNone(self.user_0.id)

    def test_create_user_profile(self):
        """Test user profile attaches to user correctly."""
        george_pr = UserProfile(user=self.user_0)
        self.assertIs(george_pr, self.user_0.profile)


class ExistingUserCase(TestCase):
    """Test if user exists."""

    def setUp(self):
        self.user_1 = UserFactory.create(
            username='jim',
            email='jim@example.com',
        )
        self.user_1.set_password('secret')

        self.user_2 = UserFactory.create(
            username='judy',
            email='judy@example.com',
        )
        self.user_2.set_password('moresecret')


    def test_user_has_profile(self):
        """Test if use has a profile."""
        self.assertTrue(self.user_1.profile)
        self.assertTrue(self.user_2.profile)

    def test_how_many_profiles(self):
        """Test number of expected User profiles."""
        self.assertEqual(len(UserProfile.objects.all()), 2)

    def test_user_active(self):
        """Test if user's profile is active."""
        self.assertTrue(self.user_1.profile in UserProfile.active.all())

    def test_profile_has_pk(self):
        """Test if profile has a primary key."""
        self.assertTrue(self.user_2.profile.pk)

    def test_expected_user_username(self):
        """Test username is as expected."""
        self.assertEqual(self.user_1.username, 'jim')

    def test_expected_email(self):
        """Test user email is as expected."""
        self.assertEqual(self.user_2.email, 'judy@example.com')

    def test_str(self):
        """Test UserProfile string method."""
        judy_pr = self.user_2.profile
        self.assertEquals(str(judy_pr), 'judy')

    def test_add_friends(self):
        """Test adding friends to a profile."""
        jim_pr = self.user_1.profile
        jim_pr.friends.add(self.user_2.profile)
        self.assertEqual(jim_pr.friends.all()[0], self.user_2.profile)
        self.assertEqual(self.user_2.profile.friends.all()[0], self.user_1.profile)

    def test_not_friends(self):
        """Test that a user is not a friend of another profile."""
        judy_pr = self.user_2.profile
        self.assertNotIn(self.user_1.profile, judy_pr.friends.all())

    def test_delete_user(self):
        """Test deleted user no longer has an Imager profile."""
        self.user_1.delete()
        self.assertNotIn(self.user_1.profile, UserProfile.objects.all())

    def test_no_profile_pk_after_delete(self):
        """Test that deleted user does not have a profile primary key."""
        self.user_1.delete()
        self.assertIsNone(self.user_1.profile.pk)


"""Test Game Model"""


class GameCase(TestCase):
    """Test if Games exists and are built correctly."""

    def setUp(self):

        self.user_1 = UserFactory.create(
            username='jim',
            email='jim@example.com',
        )
        self.user_1.set_password('secret')

        self.user_2 = UserFactory.create(
            username='judy',
            email='judy@example.com',
        )
        self.user_2.set_password('moresecret')

        self.game_1 = GameFactory.create(
            host=self.user_1.profile,
            # players=[self.user_1, self.user_2]
        )
        self.game_2 = GameFactory.create(
            host=self.user_2.profile,
            # players=[self.user_2, self.user_1]
        )
        self.user_1.profile.player_1.add(self.game_1)
        self.user_2.profile.player_2.add(self.game_1)
        self.game_1.users.add(self.game_1.player_1)
        self.game_1.users.add(self.game_1.player_2)

        self.user_1.profile.player_2.add(self.game_2)
        self.user_2.profile.player_1.add(self.game_2)
        self.game_2.users.add(self.game_2.player_1)
        self.game_2.users.add(self.game_2.player_2)

    def test_user_has_game(self):
        """Test if user has a game."""
        self.assertTrue(self.user_1.profile.games is not None)

    def test_how_many_games(self):
        """Test number of expected profiles."""
        self.assertEqual(len(Game.objects.all()), 2)

    def test_game_has_pk(self):
        """Test if profile has a primary key."""
        self.assertTrue(self.game_2.pk)

    def test_expected_player_username(self):
        """Test username is as expected."""
        self.assertEqual(self.game_1.player_1.user.username, 'jim')
        self.assertEqual(self.game_1.player_2.user.username, 'judy')
        self.assertEqual(self.game_2.player_1.user.username, 'judy')
        self.assertEqual(self.game_2.player_2.user.username, 'jim')

    def test_str(self):
        """Test UserProfile string method."""
        self.assertTrue(str(self.game_1))

    def test_mrx_in_game(self):
        self.assertTrue(self.game_1.mrx)
        self.assertTrue(self.game_2.mrx)

    def test_different_xes(self):
        self.assertIsNot(self.game_1.mrx, self.game_2.mrx)

    def test_detectives_in_game(self):
        self.assertEquals(len(self.game_1.dets.all()), 5)

    def test_round_exists(self):
        self.assertTrue(self.game_1.rounds)

    def test_turn_number(self):
        self.assertTrue(self.game_1.turn_number(), 1)

    def test_locations(self):
        self.assertTrue(self.game_1.rounds.first().mrx_loc)
        self.assertTrue(self.game_1.rounds.first().det1_loc)
        self.assertTrue(self.game_1.rounds.first().det2_loc)
        self.assertTrue(self.game_1.rounds.first().det3_loc)
        self.assertTrue(self.game_1.rounds.first().det4_loc)
        self.assertTrue(self.game_1.rounds.first().det5_loc)
