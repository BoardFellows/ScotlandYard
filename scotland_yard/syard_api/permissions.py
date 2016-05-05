from rest_framework import permissions
from rest_framework.authtoken.models import Token

from syard_api.helper import (
    get_auth_header,
    get_credentials,
    check_credentials,
)


def check_for_auth(request, obj):
    """Method to check for token or basic auth."""
    try:
        auth_header = get_auth_header(request)
        if auth_header[0] == "Token":
            auth_token = Token.objects.get(user=obj)
            return auth_token == auth_header[1]
        auth_user = check_credentials(get_credentials(auth_header))
        return auth_user == obj
    except KeyError:
        return False


class HasTokenOrBasic(permissions.BasePermission):
    """Permission class that allows access to authorized user's own info."""

    def has_object_permission(self, request, view, obj):
        """Return boolean representing object permissions."""
        return check_for_auth(request, obj)


class IsCreateOrIsAuthorized(permissions.BasePermission):
    """Permission class that allows POST method or user to access own info."""

    def has_object_permission(self, request, view, obj):
        """Return Bool representing object permissions."""
        if request.method == "POST":
            return True
        return check_for_auth(request, obj)
