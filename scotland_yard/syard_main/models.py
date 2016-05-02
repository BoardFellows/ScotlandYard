from __future__ import unicode_literals

from django.conf import settings

from django.db import models

from django.utils.encoding import python_2_unicode_compatible


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

    def turn_number(self):
        """Turn Number."""
        return self.rounds.objects.count()

    def _piece_location(self, piece):
        """
        Return most recent location of a piece.

        Accept a string with the name of the piece (color or mrx).
        """
        loc = "".join([piece, "_loc"])
        qs = self.rounds.all()

    def __str__(self):
        """Return string output of username."""
        return str(self.id)

    # def __unicode__(self):
    #     return unicode(self.some_field) or u''


@python_2_unicode_compatible
class Round(models.Model):
    game = models.ForeignKey(
        'Game',
        related_name='rounds',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    mrx_loc = models.IntegerField(null=True)
    red_loc = models.IntegerField(null=True)
    yellow_loc = models.IntegerField(null=True)
    green_loc = models.IntegerField(null=True)
    blue_loc = models.IntegerField(null=True)
    purple_loc = models.IntegerField(null=True)

    def __str__(self):
        """Return string output of username."""
        return "game: {}, turn: {}".format(str(self.game.id), str(self.id))

    def get_active_piece(self):
        """Return the piece (x, r, y, g, b, p) to move next"""
        pass

    def complete(self):
        """Return True if all rounds in field are truthy, else false."""
        pass
