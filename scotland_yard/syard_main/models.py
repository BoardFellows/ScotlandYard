from __future__ import unicode_literals

from random import randrange

from django.conf import settings

from django.db import models

from django.utils.encoding import python_2_unicode_compatible


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


@python_2_unicode_compatible
class UserProfile(models.Model):
    """Define User Profile model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile"
    )
    friends = models.ManyToManyField(
        "self",
        related_name='friend_of',
        null=True,
        blank=True,
    )
    games = models.ManyToManyField(
        "Game",
        related_name='player',
        null=True,
        blank=True,
        db_index=True
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string output of username."""
        return self.user.get_full_name() or self.user.username

    @property
    def is_active(self):
        """Return a boolean value indicating whether User is active."""
        return self._is_active


@python_2_unicode_compatible
class Game(models.Model):
    """Game model."""

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="host",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    winner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='won',
        null=True,
        default=None,
    )
    # mrx = models.OneToOneField(
    #     'MrX',
    #     related_name="game"
    # )
    # det1 = models.OneToOneField(
    #     'Detective',
    #     related_name="game"
    # )
    # det2 = models.OneToOneField(
    #     'Detective',
    #     related_name="game"
    # )
    # det3 = models.OneToOneField(
    #     'Detective',
    #     related_name="game"
    # )
    # det4 = models.OneToOneField(
    #     'Detective',
    #     related_name="game"
    # )
    # det5 = models.OneToOneField(
    #     'Detective',
    #     related_name="game"
    # )

    def __str__(self):
        """Return string output of username."""
        return str(self.id)

    def turn_number(self):
        """Turn Number."""
        return self.rounds.objects.count()

    def _piece_location(self, piece):
        """Return most recent location of a piece, identified by name."""
        loc = "".join([piece, "_loc"])
        qs = self.rounds.all()
        if qs[-1].__getattribute__(loc):
            return qs[-1].__getattribute__(loc)
        else:
            return qs[-2].__getattribute__(loc)

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

    def __str__(self):
        """Return string output of username."""
        return "game: {}, turn: {}".format(str(self.game.id), str(self.id))

    def get_active_piece(self):
        """Return the piece (x, r, y, g, b, p) to move next"""
        pass

    def complete(self):
        """Return True if all rounds in field are truthy, else false."""
        pass


@python_2_unicode_compatible
class MrX(models.Model):
    taxi = models.IntegerField(default=4)
    bus = models.IntegerField(default=3)
    underground = models.IntegerField(default=3)
    black = models.IntegerField(default=5)
    x2 = models.IntegerField(default=2)
    game = models.OneToOneField(related_name='mrx')


@python_2_unicode_compatible
class Detective(models.Model):
    taxi = models.IntegerField(default=10)
    bus = models.IntegerField(default=8)
    underground = models.IntegerField(default=4)
    game = models.OneToOneField(related_name='dets')
    role = models.CharField(choices=DETECTIVES)
