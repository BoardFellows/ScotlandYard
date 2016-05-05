from rest_framework import permissions
from rest_framework.authtoken.models import Token


class IsCreateOrIsOwner(permissions.BasePermission):
    """Permission class that allows POST method or user to access own info."""

    def has_object_permission(self, request, view, obj):
        """Return Bool representing object permissions."""
        if request.method == "POST":
            return True
        auth_token = "Token {}".format(Token.objects.get(user=obj))
        try:
            httptoken = request.META['HTTP_AUTHORIZATION']
        except KeyError:
            return False
        return auth_token == httptoken


class HasToken(permissions.BasePermission):
    """Permission class that checks for auth token."""

    def has_object_permission(self, request, view, obj):
        """Check for HTTP_AUTHORIZATION IN HEADERS."""
        try:
            httptoken = request.META['HTTP_AUTHORIZATION']
        except KeyError:
            return False
        return True
