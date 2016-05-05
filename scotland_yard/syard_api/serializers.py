from rest_framework import serializers
from django.contrib.auth.models import User
from syard_main.models import Game
from syard_api.helper import get_auth_user


class UserSerializer(serializers.ModelSerializer):
    """Serialization of Users."""

    class Meta:
        """Meta."""

        model = User
        depth = 1
        fields = (
            'id', 'username', 'email', 'password', 'profile',
        )
        # TODO: Check with F. What fields does he need?

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
            'id', 'host', 'date_created',
            'date_modified', 'player_1', 'player_2',
            'active_player', 'round_number', 'current_round', 'rounds',
            'complete', 'winner'
        )

    def create(self, validated_data):
        """Modified create method to encrypt password to save in db."""
        request = self.context['request']
        player1 = get_auth_user(request, token_only=True).profile
        player2 = User.objects.get(email=request.data['otherPlayer']).profile
        game = Game(
            host=player1,
            player1_is_x=request.data['gameCreatorIsMrX']
        )
        game.save()
        game.set_players(player1, player2)
        return game

    def update(self, instance, validated_data):
        """Update current round of game."""
        request_data = self.context['request'].data
        player_profile = get_auth_user(self.context['request'], token_only=True).profile
        if request_data['player'] == 'mrx':
            cur_node = instance.current_round.mrx_loc
        else:
            cur_node = instance.current_round.det1_loc
        next_node = request_data['nodeId']
        ticket = request_data['tokenType']
        instance.move_piece(cur_node, next_node, ticket, player_profile)
        return instance
