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
            'round_number', 'rounds',
            'complete', 'winner'
        )

    def create(self, validated_data):
        """Modified create method to encrypt password to save in db."""
        request = self.context['request']
        player1 = get_auth_user(request, token_only=True).profile
        email = request.data['otherPlayer']
        player2 = User.objects.get(email=email).profile
        game = Game(
            host=player1,
            player1_is_x=request.data['gameCreatorIsMrX'],
            player_1=player1,
        )
        game.save()
        game.set_players(player1, player2)
        return game

    def update(self, instance, validated_data):
        """Update current round of game."""
        # import pdb; pdb.set_trace()
        request_data = self.context['request'].data
        player_profile = get_auth_user(self.context['request'], token_only=True).profile
        role = request_data['player'] 
        cur_node = instance.get_locations()[role]
        next_node = int(request_data['nodeId'])
        ticket = request_data['tokenType']
        instance.move_piece(cur_node, next_node, ticket, player_profile)
        instance.save()
        print(instance.current_round.mrx_loc)
        return instance
