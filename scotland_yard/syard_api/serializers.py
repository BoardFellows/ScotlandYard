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
        fields = (
            'id', 'username', 'email', 'password', 'profile',
        )

    def create(self, validated_data):
        """Modified create method to encrypt password to save in db."""
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
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
            'active_player', 'round_number', 'current_round'
            'complete', 'winner'
        )

    def create(self, validated_data):
        """Modified create method to encrypt password to save in db."""
        request_token = self.context['request'].META['HTTP_AUTHORIZATION']
        token = Token.objects.get(key=request_token.split()[1])
        host = token.user.profile
        game = Game(
            host=host,
            player_1=host,
            player_1_is_x=self.context['request']
        )
        game.save()
        return game

    def update(self, validated_data):
        current
        

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
