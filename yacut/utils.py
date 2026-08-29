import random
import string
from flask import request  # type: ignore
from yacut.models import URLMap


def get_unique_short_id(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short = ''.join(random.choices(chars, k=length))
        is_unique = not URLMap.query.filter_by(short=short).first()
        if short != 'files' and is_unique:
            return short


def is_api_request():
    return (
        request.path.startswith('/api/')
        or request.accept_mimetypes.best == 'application/json'
    )
