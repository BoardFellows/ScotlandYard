import base64
import binascii

from django.utils.six import text_type
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import (permissions, HTTP_HEADER_ENCODING, exceptions,)
from rest_framework.authtoken.models import Token


def get_auth_header(request):
    """Get auth header and return list of key, val."""
    auth = request.META['HTTP_AUTHORIZATION']
    if isinstance(auth, text_type):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth.split()


def get_credentials(auth):
        if len(auth) == 1 or len(auth) > 2:
            msg = _('Invalid basic header. Credentials invalid or not provided.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)

        credentials = {
            'username': auth_parts[0],
            'password': auth_parts[2]
        }
        return credentials


def check_credentials(credentials):
        user = authenticate(**credentials)
        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username or password.'))
        return User.objects.get(username=credentials['username'])


class IsCreateOrIsAuthorized(permissions.BasePermission):
    """Permission class that allows POST method or user to access own info."""

    def has_object_permission(self, request, view, obj):
        """Return Bool representing object permissions."""
        if request.method == "POST":
            return True
        try:
            auth_header = get_auth_header(request)
            if auth_header[0] == "Token":
                auth_token = Token.objects.get(user=obj)
                return auth_token == auth_header[1]
            auth_user = check_credentials(get_credentials(auth_header))
            return auth_user == obj
        except KeyError:
            return False


class HasToken(permissions.BasePermission):
    """Permission class that checks for auth token."""

    def has_object_permission(self, request, view, obj):
        """Check for HTTP_AUTHORIZATION IN HEADERS."""
        try:
            return get_auth_header(request)[0] == "Token"
        except KeyError:
            return False
