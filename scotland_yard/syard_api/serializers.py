from rest_framework import serializers
from django.contrib.auth.models import User
from syard_main.models import UserProfile, Game, Round


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serialization of Users."""

    class Meta:
        """Meta."""

        model = User
        fields = ('url', 'id', 'username', 'email', 'profile')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """Serialization of Profiles."""

    def get_user(self, obj):
        """Get User."""
        return User.objects.get(user=obj.user)

    def get_friends(self, obj):
        """Get Friends."""
        return User.objects.filter(friend_of=obj.user)

    def get_games(self, obj):
        """Get Games."""
        return Game.objects.filter(user=obj.player)

    class Meta:
        """Meta."""

        model = UserProfile
        fields = ('url', 'user', 'friends', 'games')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    """Serialization of games."""
    
    # def get_players(self, obj):
    #     return User.objects.filter(user=obj.players.user)

    def get_winner(self, obj):
        return User.objects.filter(username=obj.winner.username)

    def get_round(self, obj):
        return Round.objects.filter(id=obj.id)

    class Meta:
        """Meta."""

        model = Game
        fields = ('url', 'id', 'host', 'round', 'date_created', 'date_modified', 'complete', 'winner')


class RoundSerializer(serializers.HyperlinkedModelSerializer):

    def get_game(self, obj):
        return Game.objects.get(game=obj.game)

    class Meta:
        """Meta."""

        model = Round
        fields = ('game', 'mrx_loc', 'red_loc', 'yellow_loc',
            'green_loc', 'blue_loc', 'purple_loc', 'complete')

# class PlayerSerializer(serializers.HyperlinkedModelSerializer):
#     """Serialization of Player."""

#     owner = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)
#     location = serializers.HyperlinkedRelatedField(many=False, view_name='node-detail', read_only=True)

#     class Meta:
#         """Meta."""

#         model = Player
#         fields = ('owner', 'tokens', 'location')
# player num to keep track of p1 vs p2?
# player role

# UNTOUCHABLE SERIALIZERS. These models don't change.
# class BoardSerializer(serializers.HyperlinkedModelSerializer):
#     """Serialization of Boards."""

#     nodes = serializers.HyperlinkedRelatedField(many=True, view_name='node-detail', read_only=True)

#     class Meta:
#         """Meta."""

#         model = Board
#         fields = ('nodes')

# class NodeSerializer(serializers.HyperlinkedModelSerializer):
#     """Serialization of Boards."""

#     edges = serializers.HyperlinkedRelatedField(many=True, view_name='edge-detail', read_only=True)

#     class Meta:
#         """Meta."""

#         model = Node
#         fields = ('id', 'nodeName', 'xPos', 'yPos', 'edges')


# class EdgeSerializer(serializers.HyperlinkedModelSerializer):
#     """Serialization of Boards."""

#     nodes = serializers.HyperlinkedRelatedField(many=True, view_name='node-detail', read_only=True)

#     class Meta:
#         """Meta."""

#         model = Edge
#         fields = ('type', 'nodes')
# id and weight?
