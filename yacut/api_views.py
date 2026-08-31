import re
from flask import abort, request, jsonify
from werkzeug.exceptions import BadRequest
from yacut import app, db
from yacut.constants import (
    ERROR_MESSAGES, MAX_CUSTOM_SHORT_ID_LENGTH, RESERVED_NAMES, SHORT_ID_REGEX
)
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from http import HTTPStatus


def validate_custom_id(custom_id: str) -> str:
    custom_id = custom_id.strip()
    if len(custom_id) > MAX_CUSTOM_SHORT_ID_LENGTH:
        abort(400, description=ERROR_MESSAGES['invalid_short_id'])
    if not re.match(SHORT_ID_REGEX, custom_id):
        abort(400, description=ERROR_MESSAGES['invalid_short_id'])
    if custom_id in RESERVED_NAMES:
        abort(400, description=ERROR_MESSAGES['short_id_exists'])
    if URLMap.query.filter_by(short=custom_id).first():
        abort(400, description=ERROR_MESSAGES['short_id_exists'])
    return custom_id


def parse_request_data() -> dict:
    try:
        data = request.get_json()
    except BadRequest:
        abort(400, description=ERROR_MESSAGES['missing_body'])
    if data is None:
        abort(400, description=ERROR_MESSAGES['missing_body'])
    return data


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = parse_request_data()

    url = data.get('url')
    if not url:
        abort(400, description=ERROR_MESSAGES['missing_url'])

    custom_id = data.get('custom_id', '')
    if custom_id:
        short = validate_custom_id(custom_id)
    else:
        short = get_unique_short_id()

    url_map = URLMap(original=url, short=short)
    db.session.add(url_map)
    db.session.commit()

    short_link = f'{request.host_url}{short}'
    return jsonify({'url': url, 'short_link': short_link}), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        abort(404, description=ERROR_MESSAGES['id_not_found'])
    return jsonify({'url': url_map.original}), HTTPStatus.OK
