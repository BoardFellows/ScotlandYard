from rest_framework import serializers
from django.contrib.auth.models import User
from syard_main.models import UserProfile, Game, Round
from rest_framework.authtoken.models import Token
from syard_api.permissions import get_auth_header


def get_auth_user(request):
    auth_header = get_auth_header(request)
    return Token.objects.get(key=auth_header[1]).user


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
        player1 = get_auth_user(self.context['request']).profile
        player2 = User.objects.get(email=validated_data['otherPlayer']).profile
        game = Game(
            host=player1,
            player_1_is_x=validated_data['gameCreatorIsMrX']
        )
        game.save()
        game.set_players(player1, player2)
        return game

    def update(self, instance, validated_data):
        """Update current round of game."""
        player_profile = get_auth_user(self.context['request']).profile
        if validated_data['player'] == 'mrx':
            cur_node = instance.current_round.mrx_loc
        else:
            cur_node = instance.current_round.det1_loc
        next_node = validated_data['nodeId']
        ticket = validated_data['tokenType']
        instance.move_piece(cur_node, next_node, ticket, player_profile)
        return instance


class RoundSerializer(serializers.ModelSerializer):
    """Serialization of rounds."""

    class Meta:
        """Meta."""

        model = Round
        fields = (
            'mrx_loc', 'det1_loc', 'det2_loc',
            'det3_loc', 'det4_loc', 'det5_loc', 'complete'
        )
