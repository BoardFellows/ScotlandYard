# from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from syard_api.serializers import (
    UserSerializer,
    # GameSerializer,
    # PlayerSerializer,
    # BoardSerializer,
    # NodeSerializer,
    # EdgeSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Provides list and detail actions for user view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class GameViewSet(viewsets.ModelViewSet):
    """Provides list and detail actions for user view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class BoardViewSet(viewsets.ModelViewSet):
    """Provides list and detail actions for user view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
