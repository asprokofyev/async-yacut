import random
import string
from flask import request  # type: ignore
from yacut.constants import DEFAULT_SHORT_ID_LENGTH, RESERVED_NAMES
from yacut.models import URLMap


def get_unique_short_id(length=DEFAULT_SHORT_ID_LENGTH):
    chars = string.ascii_letters + string.digits
    while True:
        short = ''.join(random.choices(chars, k=length))
        is_unique = not URLMap.query.filter_by(short=short).first()
        if short not in RESERVED_NAMES and is_unique:
            return short


def is_api_request():
    return (
        request.path.startswith('/api/')
        or request.accept_mimetypes.best == 'application/json'
    )
