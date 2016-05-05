
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
