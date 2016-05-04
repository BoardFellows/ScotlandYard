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
        depth = 1
        fields = (
            'id', 'rounds', 'host', 'date_created',
            'date_modified', 'player_1', 'player_2',
            # 'current_player',
            'turn_number',
            'complete', 'winner'
        )

    def create(self, validated_data):
        """Modified create method to encrypt password to save in db."""
        host = self.context['request'].user.profile
        game = Game(
            host=host,
            player_1=host
        )
        game.save()
        return game


class RoundSerializer(serializers.ModelSerializer):
    """Serialization of rounds."""

    class Meta:
        """Meta."""

        model = Round
        fields = (
            'mrx_loc', 'det1_loc', 'det2_loc',
            'det3_loc', 'det4_loc', 'det5_loc', 'complete'
        )


# class BoardSerializer(serializer.ModelSerializer)
# just returns the board or errors
# pass
