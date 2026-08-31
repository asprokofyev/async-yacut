from flask import jsonify, render_template  # type: ignore
from yacut import app, db
from http import HTTPStatus
from yacut.constants import ERROR_MESSAGES
from yacut.utils import is_api_request


@app.errorhandler(404)
def page_not_found(error):
    error_message = getattr(
        error, 'description', ERROR_MESSAGES['page_not_found'])
    if is_api_request():
        return jsonify(
            {'message': error_message}
        ), HTTPStatus.NOT_FOUND
    return render_template(
        '404.html', error_message=error_message
    ), HTTPStatus.NOT_FOUND


@app.errorhandler(403)
def forbidden(error):
    error_message = getattr(
        error, 'description', ERROR_MESSAGES['forbidden'])
    if is_api_request():
        return jsonify(
            {'message': error_message}
        ), HTTPStatus.FORBIDDEN
    return render_template(
        '403.html', error_message=error_message
    ), HTTPStatus.FORBIDDEN


@app.errorhandler(400)
def bad_request(error):
    error_message = getattr(
        error, 'description', ERROR_MESSAGES['bad_request'])
    if is_api_request():
        return jsonify(
            {'message': error_message}
        ), HTTPStatus.BAD_REQUEST
    return render_template(
        '400.html', error_message=error_message
    ), HTTPStatus.BAD_REQUEST


@app.errorhandler(500)
def internal_server_error(error):
    try:
        db.session.rollback()
    except Exception:
        pass

    error_message = getattr(
        error, 'description', ERROR_MESSAGES['internal_error'])
    if is_api_request():
        return jsonify(
            {'message': error_message}
        ), HTTPStatus.INTERNAL_SERVER_ERROR
    return render_template(
        '500.html', error_message=error_message
    ), HTTPStatus.INTERNAL_SERVER_ERROR
