from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.authtoken.models import Token
from rest_framework import (viewsets, status,)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from syard_api.permissions import IsCreateOrIsOwner, HasToken
from syard_api.serializers import (UserSerializer, GameSerializer,)
from syard_main.models import (Game,)
from syard_main.board import BOARD


def get_request_token(request):
    token = request.META['HTTP_AUTHENTICATION']
    return Token.objects.get(key="Token {}".format(token))


@require_GET
def board_view(request):
    """Return the Board with a get request."""
    data = BOARD
    return JsonResponse(data)


class UserViewSet(viewsets.ModelViewSet):
    """Provides actions for user view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsCreateOrIsOwner,)

    def create(self, request):
        """Create User and Send token in as header."""
        response = super(UserViewSet, self).create(request, data=request.data)
        user = User.objects.get(id=response.data['id'])
        token = Token.objects.get(user=user)
        response['authToken'] = token
        return response

    def list(self, request):
        """Disallow list method."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GameViewSet(viewsets.ModelViewSet):
    """Provides actions for user view."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (HasToken, )

    def get_queryset(self):
        """Get all games belonging to user whose Auth Token was sent in headers."""
        try:
            token = self.request.META['HTTP_AUTHORIZATION'].split()[1]
            usertoken = Token.objects.get(key=token)
            user = usertoken.user
        except KeyError:
            return
        return Game.objects.filter(host=user.profile)
