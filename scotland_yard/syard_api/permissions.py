from rest_framework import permissions
from rest_framework.authtoken.models import Token

    
class IsCreateOrIsOwner(permissions.BasePermission):
    """Permission class that allows POST method or user to access own info."""

    def has_object_permission(self, request, view, obj):
        """Return Bool representing object permissions."""
        if request.method == "POST":
            return True

        token = Token.objects.get(user=obj.user)
        return token == request['Authentication'][7:]
