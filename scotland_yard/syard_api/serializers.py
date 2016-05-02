from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serialization of Users."""

    # games = serializers.HyperlinkedRelatedField(many=True, view_name='game-detail', read_only=False)
    # friends = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=False)

    class Meta:
        """Meta."""

        model = User
        fields = ('url', 'id', 'username', 'email')
        # add games and friends


# class GameSerializer(serializers.HyperlinkedModelSerializer):
#     """Serialization of games."""

#     players = serializers.HyperlinkedRelatedField(many=True, view_name='player-detail', read_only=True)
#     users = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
#     winner = serializers.HyperlinkedRelatedField(many=False, view_name='winner-detail', read_only=False)
#     # do we want players or users?

#     class Meta:
#         """Meta."""

#         model = Game
#         fields = ('url', 'id', 'players', 'users', 'turns', 'complete', 'winner')


# class BoardSerializer(serializers.HyperlinkedModelSerializer):
#     """Serialization of Boards."""

#     nodes = serializers.HyperlinkedRelatedField(many=True, view_name='node-detail', read_only=True)

#     class Meta:
#         """Meta."""

#         model = Board
#         fields = ('id', nodes')
# do we want an id on this field?


# class PlayerSerializer(serializers.HyperlinkedModelSerializer):
#     """Serialization of Boards."""

#     owner = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)
#     location = serializers.HyperlinkedRelatedField(many=False, view_name='node-detail', read_only=True)

#     class Meta:
#         """Meta."""

#         model = Player
#         fields = ('owner', 'tokens', 'location')
# player num to keep track of p1 vs p2?
# player role


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
