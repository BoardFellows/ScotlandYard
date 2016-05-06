from __future__ import unicode_literals

from random import randrange

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from syard_main.board import BOARD


DETECTIVES = [
    ('det1', 'det1'),
    ('det2', 'det2'),
    ('det3', 'det3'),
    ('det4', 'det4'),
    ('det5', 'det5'),
]

STARTING_NODES = [
    13, 26, 29, 34, 50, 53, 91, 94, 103,
    112, 117, 132, 138, 141, 155, 174, 197, 198
]


class ActiveUserManager(models.Manager):
    """Query User Profile attached to an active user."""

    def get_queryset(self):
        """Return query set of profiles with active users."""
        queryset = super(ActiveUserManager, self).get_queryset()
        return queryset.filter(user__is_active=True)


@python_2_unicode_compatible
class UserProfile(models.Model):
    """Define User Profile model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        null=True
    )
    friends = models.ManyToManyField(
        "self",
        related_name='friends',
        blank=True,
    )
    games = models.ManyToManyField(
        "Game",
        related_name='users',
        blank=True,
        db_index=True
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string output of username."""
        return self.user.username

    # @property
    # def is_active(self):
    #     """Return a boolean value indicating whether User is active."""
    #     return self._is_active

    active = ActiveUserManager()
    objects = models.Manager()


@python_2_unicode_compatible
class Game(models.Model):
    """Game model."""

    host = models.ForeignKey(
        UserProfile,
        related_name="host",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    winner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='won',
        null=True,
    )

    player_1 = models.ForeignKey(
        UserProfile,
        related_name='player_1',
        null=True,
        blank=True
    )

    player_2 = models.ForeignKey(
        UserProfile,
        related_name='player_2',
        null=True,
        blank=True
    )

    player1_is_x = models.BooleanField(default=True)

    def __str__(self):
        """Return string output of username."""
        return str(self.id)

    def _piece_location(self, piece):
        """Return most recent location of a piece, identified by name."""
        loc = "".join([piece, "_loc"])
        qs = self.rounds.all()
        if qs.reverse()[0].__getattribute__(loc):
            return qs.reverse()[0].__getattribute__(loc)
        else:
            return qs.reverse()[1].__getattribute__(loc)

    def get_locations(self):
        """Return a dictionary with the location of each piece on the board."""
        return {
            'mrx': self._piece_location('mrx'),
            'det1': self._piece_location('det1'),
            'det2': self._piece_location('det2'),
            'det3': self._piece_location('det3'),
            'det4': self._piece_location('det4'),
            'det5': self._piece_location('det5'),
        }

    def _start_node_list(self):
        """Return 6 non-repeating values from the STARTING_NODES list."""
        starts = list(STARTING_NODES)
        output = [starts.pop(randrange(0, len(starts))) for x in range(6)]
        return output

    @property
    def round_number(self):
        """Turn Number."""
        return self.rounds.count() - 1

    @property
    def current_round(self):
        if self.rounds.latest('date_modified').complete:
            self.make_new_round()
        return self.rounds.latest('date_modified')

    @property
    def active_piece(self):
        """Return the piece to move next"""
        current_round = self.rounds.latest('date_modified')
        return current_round.active_piece

    @property
    def active_player(self):
        return self._active_player()

    def _active_player(self):
        if (
            ((self.active_piece == 'mrx') and self.player1_is_x) or
            ((self.active_piece != 'mrx') and not self.player1_is_x)
        ):
            return self.player_1
        else:
            return self.player_2

    def _x_wins_by_turns(self):
        """Check for Game Over by number of turns, to be used below."""
        if self.rounds.latest('date_modified').complete and self.round_number == 22:
            return True
        else:
            return False

    def make_new_round(self):
        """Add a new round if round complete and new round needed."""
        if self._x_wins_by_turns():
            return 'X Wins.'
        current_round = self.rounds.latest('date_modified')
        if current_round.complete:
            new_round = Round(game=self, num=(self.round_number + 1))
            new_round.save()
            return new_round.active_piece
        return current_round.active_piece

    def set_players(self, user_profile_1, user_profile_2):
        """Takes two profiles, sets them as players of the game."""
        user_profile_1.player_1.add(self)
        user_profile_2.player_2.add(self)
        self.users.add(self.player_1)
        self.users.add(self.player_2)

    def move_piece(self, id1, id2, ticket, user_profile):
        self.current_round
        if self.validate_move(id1, id2, ticket, user_profile) is True:
            if self.active_piece == 'mrx':
                current = self.rounds.latest('date_modified')
                current.mrx_loc = id2
                current.save()
                # self._move_helper(self.mrx, ticket)
            else:
                current = self.current_round
                current.__setattr__(self.active_piece + '_loc', id2)
                piece = self.dets.get(role=self.active_piece)
                num = getattr(self.mrx, ticket)
                num += 1
                setattr(self.mrx, ticket, num)
                self.save()
                self.mrx.save()
                self._move_helper(piece, ticket)
                current.save()
                if self._x_wins_by_turns():
                    if self.player1_is_x:
                        return self.player1
                    else:
                        return self.player2
        else:
            return self.validate_move(id1, id2, ticket, user_profile)

    def _move_helper(self, piece, ticket):
        num = getattr(piece, ticket)
        num -= 1
        setattr(piece, ticket, num)
        piece.save()

    """MAIN MOVE VALIDATOR"""

    def validate_move(self, id1, id2, ticket, user_profile):
        """Return True if move is validated."""
        #  TODO: Figure out how to catch error messages as they bubble up.
        occupied = self.get_locations()
        if self._wrong_player(user_profile):
            return "NOTYA TURN"
        try:
            self._wrong_piece(id1)
        except ValueError:
            return "YA DONE GOOFED"
        try:
            self._invalid_move(id1, id2)
        except KeyError:
            return "YA DONE GOOFED."
        if not self._legal_move(id1, id2, ticket):
            return "YA DONE GOOFED."
        if not self._has_ticket(ticket):
            return "YA BROKE, SON."
        if self._check_capture(id2, occupied):
            return self._check_capture(id2, occupied)
        if self._space_occupied(id1, id2, occupied):
            return self._space_occupied(id1, id2, occupied)
        return True

    """VALIDATION HELPER METHODS"""

    def _wrong_player(self, user_profile):
        if user_profile is not self.active_player:
            return "wrong player"

    def _wrong_piece(self, id1):
        """Validate id1 against location of active piece."""
        if self._piece_location(self.active_piece) != id1:
            msg = ("It is {}'s move. {} is at space {}.".format(
                self.active_piece,
                self.active_piece,
                self._piece_location(self.active_piece)
            ))
            raise ValueError(msg)

    def _invalid_move(self, id1, id2):
        """Check that start and end locations are on the board."""
        try:
            BOARD[id1]
        except KeyError:
            raise KeyError('Your start location is not on the board.')
        try:
            BOARD[id2]
        except KeyError:
            raise KeyError('Your end location is not on the board.')

    def _legal_move(self, id1, id2, ticket):
        """Check that start and end nodes are connected by ticket method."""
        if ticket is not "black":
            return True if id2 in BOARD[id1][ticket] else False
        else:
            for ticket in BOARD[id1]:
                if id2 in BOARD[id1[ticket]]:
                    return True
            return False

    def _has_ticket(self, ticket):
        """Check that the piece to be moved as an appropriate ticket"""
        if self.active_piece == 'mrx':
            return True if self.mrx.__getattribute__(ticket) > 0 else False
        else:
            d = self.dets.get(role=self.active_piece)
            return True if d.__getattribute__(ticket) > 0 else False

    def _real_move(self, id1, id2):
        """Check that a proposed move is actually a move"""
        return True if id1 != id2 else False

    def _check_capture(self, id2, occupied):
        """Check if a detective has moved on to mrx - if yes, return player"""
        occupied = self.get_locations()
        if self.active_piece == 'mrx':
            for name, value in occupied.items():
                if id2 == value:
                    if self.player1_is_x:
                        return self.player_2
                    else:
                        return self.player_1

        if id2 == occupied['mrx']:
            return self.active_player

    def _space_occupied(self, id1, id2, occupied):
        for name, id in occupied.items():
            if id2 == id:
                return "location {} is occupied by {}".format(id, name)


@python_2_unicode_compatible
class Round(models.Model):
    game = models.ForeignKey(
        'Game',
        related_name='rounds',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    mrx_loc = models.IntegerField(null=True)
    det1_loc = models.IntegerField(null=True)
    det2_loc = models.IntegerField(null=True)
    det3_loc = models.IntegerField(null=True)
    det4_loc = models.IntegerField(null=True)
    det5_loc = models.IntegerField(null=True)
    num = models.IntegerField(default=0)

    def __str__(self):
        """Return string output of username."""
        return "game: {}, turn: {}".format(str(self.game.id), str(self.id))

    @property
    def active_piece(self):
        return self._active_piece()

    def _active_piece(self):
        """Return the piece to move next"""
        if not self.mrx_loc:
            return 'mrx'
        if not self.det1_loc:
            return 'det1'
        if not self.det2_loc:
            return 'det2'
        if not self.det3_loc:
            return 'det3'
        if not self.det4_loc:
            return 'det4'
        if not self.det5_loc:
            return 'det5'

    @property
    def complete(self):
        """Return True if all rounds in field are truthy, else false."""
        if not self._active_piece():
            return True


@python_2_unicode_compatible
class MrX(models.Model):
    game = models.OneToOneField('Game', related_name='mrx', null=True)
    taxi = models.IntegerField(default=4)
    bus = models.IntegerField(default=3)
    underground = models.IntegerField(default=3)
    black = models.IntegerField(default=5)
    x2 = models.IntegerField(default=2)

    def __str__(self):
        """Return string output of MrX."""
        return "game: {}, turn: {}, position: {}".format(
            str(self.game.id),
            str(self.game.round_number),
            str(self.game._piece_location('mrx'))
        )


@python_2_unicode_compatible
class Detective(models.Model):
    game = models.ForeignKey('Game', related_name='dets')
    role = models.CharField(max_length=10, choices=DETECTIVES, null=True, default=None)
    taxi = models.IntegerField(default=10)
    bus = models.IntegerField(default=8)
    underground = models.IntegerField(default=4)

    def __str__(self):
        """Return string output of a detective."""
        return "game: {}, turn: {}, position: {}".format(
            str(self.game.id),
            str(self.game.round_number),
            str(self.game._piece_location('{}'.format(self.role)))
        )
