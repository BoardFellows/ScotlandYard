from rest_framework import serializers
from django.contrib.auth.models import User
from syard_main.models import UserProfile, Game, Round


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serialization of Users."""

    class Meta:
        """Meta."""

        model = User
        fields = ('url', 'id', 'username', 'email',)


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """Serialization of Profiles."""

    class Meta:
        """Meta."""

        model = UserProfile
        fields = ('url', 'user', 'friends', 'games')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    """Serialization of games."""

    class Meta:
        """Meta."""

        model = Game
        fields = ('url', 'id', 'rounds', 'host', 'date_created', 'date_modified', 'complete', 'winner')


class RoundSerializer(serializers.HyperlinkedModelSerializer):
    """Serialization of rounds."""

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
