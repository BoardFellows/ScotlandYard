from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET

from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from syard_api.permissions import IsCreateOrIsAuthorized, HasToken
from syard_api.helper import get_auth_user
from syard_api.serializers import UserSerializer, GameSerializer
from syard_main.models import Game
from syard_main.board import BOARD


def home_view(request, *args, **kwargs):
    """Basic home landing view."""
    welcome = "Welcome GameFellows!"
    return HttpResponse(welcome)


@require_GET
def board_view(request):
    """View for the basic board.

    GET /boards/ returns a JSON representation of the game board.
    """
    data = BOARD
    return JsonResponse(data)


class UserViewSet(viewsets.ModelViewSet):
    """Class for views involving the user.

    GET /users/ acts as a login screen. If provided with Basic Auth,
    it returns that particular user's information in the body of the request
    and an 'authToken' in the header.

    POST /users/ creates a new user. It then displays the user's info
    in the body of the request and sends an 'authToken' in the header.

    'GET' /users/:id returns the authorized user's information and NOT
    the 'authTokens'

    'PUT' /users/:id updates an authorized user.

    'DELETE' /users/:id deletes the authorized user.

    """

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
        user = get_auth_user(request)
        serializer = self.get_serializer(user)
        response = Response(serializer.data)
        response['authToken'] = Token.objects.get(user=user)
        return response


class GameViewSet(viewsets.ModelViewSet):
    """Class for views involving the game.

    GET /games/ returns a list of the authorized user's games.
    POST /games/ allows the authorized user to start a games.
    GET /games/:id provides the current game state if the auth
        user is a player in the game.
    PUT /games/:id puts in a reqest to update the game state.

    Technically no permissions for these views, however, 
    the queryset is restricted to only games that the authenticated
    user is a part of. Will not show a 401/403, simply a detail not found.
    """

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        """Get all games belonging to user whose Auth Token was sent in headers."""
        return get_auth_user(self.request).profile.games
