from rest_framework import permissions
from syard_api.helper import get_auth_user


def check_for_auth(request, obj, token_only):
    """Method to check for token or basic auth."""
    try:
        return obj == get_auth_user(request, token_only)
    except KeyError:
        return False


class HasToken(permissions.BasePermission):
    """Permission class that allows access to authorized user's own info."""

    def has_object_permission(self, request, view, obj):
        """Return boolean representing object permissions."""
        return check_for_auth(request, obj, token_only=True)


class IsCreateOrIsAuthorized(permissions.BasePermission):
    """Permission class that allows POST method or user to access own info."""

    def has_object_permission(self, request, view, obj):
        """Return Bool representing object permissions."""
        if request.method == "POST":
            return True
        return check_for_auth(request, obj)
