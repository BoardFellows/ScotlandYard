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
            'id', 'username', 'email', 'profile',
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

    locations = serializers.SerializerMethodField()

    def get_locations(self, obj):
        return obj.get_locations

    class Meta:
        """Meta."""

        model = Game
        depth = 1
        fields = (
            'id', 'host', 'date_created',
            'date_modified', 'player_1', 'player_2',
            'round_number', 'rounds', 'locations',
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
        )
        game.save()
        game.set_players(player1, player2)
        return game

    def update(self, instance, validated_data):
        """Update current round of game."""
        request = self.context['request']
        player_profile = get_auth_user(request, token_only=True).profile
        role = request.data['player']
        cur_node = instance.get_locations()[role]
        next_node = int(request.datadata['nodeId'])
        ticket = request_data['tokenType']
        instance.move_piece(cur_node, next_node, ticket, player_profile)
        instance.save()
        return instance
