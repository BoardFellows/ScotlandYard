# from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.authtoken.models import Token
from rest_framework import (
    viewsets,
    permissions,
    status,

)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from syard_api.permissions import IsCreateOrIsOwner
# from django.shortcuts import get_object_or_404
from syard_main.models import (
    # UserProfile,
    Game,
    # Round
)
from syard_api.serializers import (
    UserSerializer,
    # ProfileSerializer,
    GameSerializer,
    # RoundSerializer,
    # BoardSerializer,
)


@require_GET
def board_view(request):
    """Return the Board with a get request."""
    data = {'board': {'a': 'b'}}
    return JsonResponse(data)

class UserViewSet(viewsets.ModelViewSet):
    """Provides actions for user view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsCreateOrIsOwner,)

    def create(self, request):
        print(request.data)
        response = super(UserViewSet, self).create(request, data=request.data)
        user = User.objects.get(id=response.data['id'])
        token = Token.objects.get(user=user)
        response['authToken'] = token
        return response

    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class GameViewSet(viewsets.ModelViewSet):
    """Provides actions for user view."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer
