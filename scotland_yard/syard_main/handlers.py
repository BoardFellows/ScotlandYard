"""Signal handlers registered by imager_profile app."""
from __future__ import unicode_literals

import logging

from django.conf import settings

from django.db.models.signals import post_save, pre_delete

from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from syard_main.models import Detective, Game, MrX, Round, UserProfile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def make_user_profile(sender, **kwargs):
    """Create a related user profile when a new user is created."""
    if kwargs.get('created', False):
        try:
            new_profile = UserProfile(user=kwargs['instance'])
            new_profile.save()
        except(KeyError, ValueError):
            msg = 'Unable to create Profile for {}'
            logger.error(msg.format(kwargs['instance']))


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def remove_user_profile(sender, **kwargs):
    """Delete user profile when user is deleted."""
    try:
        kwargs['instance'].profile.delete()
    except (AttributeError):
        msg = (
            'Profile instance not deleted for {}.'
        )
        logger.warn(msg.format(kwargs['instance']))


@receiver(post_save, sender=Game)
def make_piece_models(sender, instance, **kwargs):
    #  TODO: Refactor this to make it less butt ugly.
    """Add pieces and starting locations to a board."""
    if kwargs.get('created', False):
        # try:
        starts = instance._start_node_list()
        mrx = MrX(game=instance)
        det1 = Detective(game=instance, role='det1')
        det2 = Detective(game=instance, role='det2')
        det3 = Detective(game=instance, role='det3')
        det4 = Detective(game=instance, role='det4')
        det5 = Detective(game=instance, role='det5')
        round1 = Round(
            game=instance,
            mrx_loc=starts.pop(),
            det1_loc=starts.pop(),
            det2_loc=starts.pop(),
            det3_loc=starts.pop(),
            det4_loc=starts.pop(),
            det5_loc=starts.pop(),
            num=0
        )
        mrx.save()
        det1.save()
        det2.save()
        det3.save()
        det4.save()
        det5.save()
        round1.save()

        # except(KeyError, ValueError):
        #     msg = 'Unable to create Profile for {}'
        #     logger.error(msg.format(kwargs['instance']))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
