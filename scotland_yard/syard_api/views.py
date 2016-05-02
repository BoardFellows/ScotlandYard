# from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from syard_api.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Provides list and detail actions for user view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
