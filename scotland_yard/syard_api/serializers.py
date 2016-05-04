from rest_framework import serializers
from django.contrib.auth.models import User
from syard_main.models import UserProfile, Game, Round
from rest_framework.authtoken.models import Token



class ProfileSerializer(serializers.ModelSerializer):
    """Serialization of Profiles."""

    class Meta:
        """Meta."""

        model = UserProfile
        fields = ('friends', 'games')


class UserSerializer(serializers.ModelSerializer):
    """Serialization of Users."""

    profile = ProfileSerializer()

    class Meta:
        """Meta."""

        model = User
        depth = 1
        fields = ('id', 'username', 'email', 'password', 'profile')

    def create(self, validated_data):
        """Modified create method to encrypt password to save in db."""
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        UserProfile.objects.create(user=user)
        return user


class GameSerializer(serializers.ModelSerializer):
    """Serialization of games."""

    class Meta:
        """Meta."""

        model = Game
        fields = ('url', 'id', 'rounds', 'host', 'date_created', 'date_modified', 'complete', 'winner')


class RoundSerializer(serializers.ModelSerializer):
    """Serialization of rounds."""

    class Meta:
        """Meta."""

        model = Round
        fields = (
            'game', 'mrx_loc', 'red_loc', 'yellow_loc',
            'green_loc', 'blue_loc', 'purple_loc', 'complete'
        )

# class BoardSerializer(serializer.ModelSerializer)
# just returns the board or errors
# pass
