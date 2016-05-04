# from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from syard_main.models import UserProfile, Game, Round
from syard_api.serializers import (
    UserSerializer,
    ProfileSerializer,
    GameSerializer,
    RoundSerializer,
    # PlayerSerializer,
    # BoardSerializer,
    # NodeSerializer,
    # EdgeSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Provides actions for user view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """Provides actions for profile view."""

    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer


class GameViewSet(viewsets.ModelViewSet):
    """Provides actions for user view."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer


class RoundViewSet(viewsets.ModelViewSet):
    """Provides actions for user view."""

    queryset = Round.objects.all()
    serializer_class = RoundSerializer
