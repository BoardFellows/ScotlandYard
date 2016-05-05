import base64
import binascii

from django.utils.six import text_type
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authtoken.models import Token


def get_auth_user(request):
    auth_header = get_auth_header(request)
    print(auth_header)
    if auth_header[0] == b'Token':
        return get_token_auth_user(auth_header)
    elif auth_header[0] == b'Basic':
        return get_basic_auth_user(auth_header)


def get_token_auth_user(auth_header):
    return Token.objects.get(key=auth_header[1]).user


def get_basic_auth_user(auth_header):
    return check_credentials(get_credentials(auth_header))


def get_auth_header(request):
    """Get auth header and return as list split on white space."""
    try:
        auth = request.META['HTTP_AUTHORIZATION']
        if isinstance(auth, text_type):
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth.split()
    except KeyError:
        raise exceptions.AuthenticationFailed('No Authorization')


def get_credentials(auth):
    """Decode auth header and return username and password.

    If not valid basic auth header, raise exception.
    """
    if len(auth) == 1 or len(auth) > 2:
        msg = _('Invalid basic header. Credentials invalid or not provided.')
        raise exceptions.AuthenticationFailed(msg)

    try:
        auth_credentials = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
    except (TypeError, UnicodeDecodeError, binascii.Error):
        msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
        raise exceptions.AuthenticationFailed(msg)

    credentials = {
        'username': auth_credentials[0],
        'password': auth_credentials[2]
    }
    return credentials


def check_credentials(credentials):
    """Authenticate credentials -- if successful, return user."""
    user = authenticate(**credentials)
    if user is None:
        raise exceptions.AuthenticationFailed(_('Invalid username or password.'))
    return user
