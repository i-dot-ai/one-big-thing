import base64
import binascii
import logging

from django.conf import settings
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class InvalidAuthError(Exception):
    pass


def get_auth_from_header(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if not auth_header:
        raise InvalidAuthError("No auth header set")
    if isinstance(auth_header, str):
        auth_header = auth_header.encode("utf-8")
    if b" " not in auth_header:
        raise InvalidAuthError("No space in header")
    auth_type, auth_value = auth_header.split(maxsplit=1)
    if auth_type.lower() != b"basic":
        raise InvalidAuthError("Not basic auth")
    try:
        auth_decoded = base64.b64decode(auth_value).decode("utf-8")
        username, password = auth_decoded.split(":", 1)
    except (TypeError, ValueError, UnicodeDecodeError, binascii.Error):
        raise InvalidAuthError("Basic auth incorrectly base64 encoded")

    return (username, password)


def make_unauthorized_response():
    return HttpResponse("Unauthorized", status=401, headers={"WWW-Authenticate": 'Basic realm="site"'})


def basic_auth_middleware(get_response):
    auth_values = settings.BASIC_AUTH.split(",")
    auth_pairs = tuple(v.split(":", 1) for v in auth_values)
    auth_map = {k: v for (k, v) in auth_pairs}

    def middleware(request):
        try:
            username, password = get_auth_from_header(request)
        except InvalidAuthError as e:
            logger.error(repr(e))
            username = None

        if username and (username in auth_map) and (auth_map[username] == password):
            response = get_response(request)
        else:
            response = make_unauthorized_response()

        return response

    return middleware
