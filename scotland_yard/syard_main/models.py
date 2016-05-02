from __future__ import unicode_literals

from django.conf import settings

from django.db import models

from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class UserProfile(models.Model):
    """Define User Profile model"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile"
    )
    friends = models.ManyToManyField(
        "self",
        null=True,
        blank=True,
    )
    games = models.ManyTomanyField(
        "Game",
        related_name='player',
        null=True,
        Blank=True,
        db_index=True
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string output of username."""
        return self.user.get_full_name() or self.username

    @property
    def is_active(self):
        """
        Return a boolean value indicating
        whether the profile's user is active.
        """
        return self._is_active


@python_2_unicode_compatible
class Game(models.Model):
    host = models.ForeignKey(
        user=settings.AUTH_USER_MODEL,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    winner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        default=None,
    )


@python_2_unicode_compatible
class Round(models.Model):
    game = models.ForeignKey(
        game=Game,
        default=0)
    mrx_loc = models.IntegerField(null=True)
    red_loc = models.IntegerField(null=True)
    yellow_loc = models.IntegerField(null=True)
    green_loc = models.IntegerField(null=True)
    blue_loc = models.IntegerField(null=True)
    purple_loc = models.IntegerField(null=True)

    def get_active_piece(self):
        """Return the piece (x, r, y, g, b, p) to move next"""
        pass

    def complete(self):
        """Return True if all rounds in field are truthy, else false."""
        pass
