from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase

import factory

from syard_main.board import BOARD

from syard_main.models import Detective, Game, MrX, Round, STARTING_NODES, UserProfile

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
        self.assertEqual(self.user_2.profile.friends.all()[0],
                         self.user_1.profile)

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

    def test_round_number(self):
        self.assertEquals(self.game_1.round_number, 0)

    def test_locations(self):
        self.assertTrue(self.game_1.rounds.first().mrx_loc)
        self.assertTrue(self.game_1.rounds.first().det1_loc)
        self.assertTrue(self.game_1.rounds.first().det2_loc)
        self.assertTrue(self.game_1.rounds.first().det3_loc)
        self.assertTrue(self.game_1.rounds.first().det4_loc)
        self.assertTrue(self.game_1.rounds.first().det5_loc)

    def test_valid_locations(self):
        self.assertIn(self.game_1.rounds.first().mrx_loc, STARTING_NODES)
        self.assertNotEqual(self.game_1.rounds.first().mrx_loc,
                            self.game_1.rounds.first().det2_loc)

    def test_get_locations(self):
        locations = self.game_1.get_locations()
        for key, value in locations.items():
            self.assertIn(value, STARTING_NODES)

"""TEST MODEL METHODS"""


class MethodsCase(TestCase):
    """Test methods on game and round that check and modify game state."""
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
        )

        self.user_1.profile.player_1.add(self.game_1)
        self.user_2.profile.player_2.add(self.game_1)
        self.game_1.users.add(self.game_1.player_1)
        self.game_1.users.add(self.game_1.player_2)

    def test_round_complete(self):
        """Test that setup round is complete."""
        self.assertTrue(self.game_1.rounds.latest('date_modified').complete)

    def test_new_round(self):
        """Add new round, test counts."""
        next_piece = self.game_1.make_new_round()
        self.assertEqual(next_piece, 'mrx')
        self.assertEqual(self.game_1.round_number, 1)
        self.assertEqual(self.game_1.rounds.count(), 2)

    def test_current_player(self):
        """Add new round, test player, update round, test player again."""
        next_piece = self.game_1.make_new_round()
        self.assertEqual(next_piece, 'mrx')
        self.assertIs(self.game_1.active_player, self.user_1.profile)
        self.assertIsNot(self.game_1.active_player, self.user_2.profile)
        rnd = self.game_1.rounds.latest('date_modified')
        rnd.mrx_loc = 75
        rnd.save()
        self.assertEqual(rnd.active_piece, 'det1')
        self.assertIs(self.game_1.active_player, self.user_2.profile)
        self.assertIsNot(self.game_1.active_player, self.user_1.profile)

    def test_move_piece(self):
        """Add new round, move mrx, add new round, make legal move with mrx."""
        rnd = self.game_1.current_round
        rnd.mrx_loc = 75
        rnd.save()
        new_round = Round(game=self.game_1, num=(self.game_1.round_number + 1))
        new_round.save()
        self.game_1.move_piece(75, 94, 'taxi', self.user_1.profile)
        rnd = self.game_1.current_round
        self.assertIs(94, rnd.mrx_loc)

    def test_move_det(self):
        """Add new round, move mrx & det1, add new round, make legal move with mrx & det1, test that det1 moved and ticket was subtracted."""
        current = self.game_1.current_round
        current.mrx_loc = 75
        current.save()
        piece = self.game_1.active_piece
        d1 = self.game_1.dets.get(role=piece)
        rnd = self.game_1.current_round
        rnd.__setattr__(piece + '_loc', 1)
        rnd.save()
        new_round = Round(game=self.game_1, num=(self.game_1.round_number + 1))
        new_round.save()
        self.game_1.move_piece(75, 94, 'taxi', self.user_1.profile)
        self.game_1.move_piece(1, 8, 'taxi', self.user_2.profile)
        rnd = self.game_1.current_round
        target = rnd.det1_loc
        self.assertIs(8, target)
        d1 = self.game_1.dets.get(role=piece)
        self.assertEquals(d1.taxi, 9)

    def test_move_validation(self):
        """Checking move validator"""
        current_round = self.game_1.current_round
        current_round.mrx_loc = 75
        current_round.save()
        self.game_1.make_new_round()
        #  tests that a move to an unconnected node fails
        self.game_1.move_piece(75, 1, 'taxi', self.user_1.profile)
        self.assertIsNot(1, current_round.mrx_loc)
        self.game_1.move_piece(75, 94, 'underground', self.user_1.profile)
        #  tests that a move to a node unconnected by a specific type fails
        self.assertIsNot(94, current_round.mrx_loc)
        self.game_1.move_piece(75, 300, 'taxi', self.user_1.profile)
        #  tests that a move off the board fails
        self.assertIsNot(300, current_round.mrx_loc)
        self.game_1.mrx.taxi = 0
        self.game_1.move_piece(75, 94, 'taxi', self.user_1.profile)
        #  tests that a valid move without a matching ticket fails
        self.assertIsNot(94, current_round.mrx_loc)

    def test__wrong_player(self):

        rnd = self.game_1.current_round
        rnd.mrx_loc = 75
        self.game_1.make_new_round()
        player = self.game_1.active_player
        wrong_player = self.game_1.player_2 if player == self.game_1.player_1 else self.game_1.player_1
        self.game_1.move_piece(75, 94, 'taxi', wrong_player)
        self.assertIsNot(94, rnd.mrx_loc)
        self.assertIs(75, rnd.mrx_loc)


"""Test BOARD"""


class BoardCase(TestCase):
    """Test that all routes on nodes with routes on partner nodes."""
    def setUp(self):

        self.board = BOARD

    def test_board_integrity(self):
        """Confirm that every connection is symmetrical"""
        for node_name, node in self.board.items():
            for travel_type, destinations in node.items():
                for destination in destinations:
                    """Assert that node does not contain itself."""
                    self.assertNotEqual(node_name, destination)
                    """Assert that connections are symmetrical"""
                    self.assertIn(node_name, self.board[destination][travel_type])

    def test_board_is_connected(self):
        """Ensure that there are no unconnected islands on the board"""
        visited = set()
        stack = [next(iter(self.board))]
        # perform a depth-first traversal
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbors in self.board[node].values():
                    stack.extend(neighbors)
        # check that we visited all the nodes
        self.assertEqual(len(visited), len(self.board))
