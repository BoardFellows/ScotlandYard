from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serialization of users."""

    friends = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    games = serializers.HyperlinkedRelatedField(many=True, view_name='game-detail', read_only=True)

    class Meta:
        """Meta."""

        model = User
        fields = ('url', 'username', 'friends', 'games', 'email')
