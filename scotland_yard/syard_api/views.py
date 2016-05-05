from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET

from rest_framework import (viewsets, status)
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from syard_api.permissions import (
    IsCreateOrIsAuthorized,
    HasToken,
    check_credentials,
    get_credentials,
    get_auth_header,
)
from syard_api.serializers import (UserSerializer, GameSerializer,)
from syard_main.models import (Game,)
from syard_main.board import BOARD


@require_GET
def board_view(request):
    """Return the Board with a get request."""
    data = BOARD
    return JsonResponse(data)


class UserViewSet(viewsets.ModelViewSet):
    """Provides actions for user view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCreateOrIsAuthorized,)

    def create(self, request):
        """Create User and Send token in as header."""
        response = super(UserViewSet, self).create(request, data=request.data)
        user = User.objects.get(id=response.data['id'])
        response['authToken'] = Token.objects.get(user=user)
        return response

    def list(self, request):
        """Repurpose list method for authenticating user credentials and redirecting/providing authToken."""
        try:
            user = check_credentials(get_credentials(get_auth_header(request)))
        except KeyError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(user)
        response = Response(serializer.data)
        response['authToken'] = Token.objects.get(user=user)
        return response


class GameViewSet(viewsets.ModelViewSet):
    """Provides actions for user view."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (HasToken, IsCreateOrIsAuthorized)

    def get_queryset(self):
        """Get all games belonging to user whose Auth Token was sent in headers."""
        try:
            token = Token.objects.get(key=get_auth_header(self.request)[1])
        except KeyError:
            return
        return Game.objects.filter(host=token.user.profile)
