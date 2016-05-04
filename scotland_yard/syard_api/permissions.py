from rest_framework import permissions

    
class IsCreateOrIsOwner(permissions.BasePermission):
    """Permission class that allows POST method or user to access own info."""

    def has_object_permission(self, request, view, obj):
        """Return Bool representing object permissions."""
        if request.method == "POST":
            return True

        # token = Token.objects.get(token=request['Authentication'][7:])
        # user = token.user
        # return obj == user
        return obj.user == request.user
