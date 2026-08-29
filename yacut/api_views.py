import re
from flask import abort, request, jsonify
from werkzeug.exceptions import BadRequest
from yacut import app, db
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from http import HTTPStatus


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    try:
        data = request.get_json()
    except BadRequest:
        abort(400, description='Отсутствует тело запроса')
    url = data.get('url')
    if not url:
        abort(400, description='"url" является обязательным полем!')
    custom_id = data.get('custom_id', '').strip()
    if custom_id:
        if len(custom_id) > 16:
            abort(
                400,
                description='Указано недопустимое имя для короткой ссылки'
            )
        if not re.match(r'^[A-Za-z0-9]+$', custom_id):
            abort(
                400,
                description='Указано недопустимое имя для короткой ссылки'
            )
        if custom_id == 'files':
            abort(
                400,
                description='Предложенный вариант короткой ссылки '
                'уже существует.'
            )
        if URLMap.query.filter_by(short=custom_id).first():
            abort(
                400,
                description='Предложенный вариант короткой ссылки '
                'уже существует.'
            )
        short = custom_id
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
        abort(404, description='Указанный id не найден')
    return jsonify({'url': url_map.original}), HTTPStatus.OK
