import re
from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField, SubmitField, MultipleFileField  # type: ignore
from wtforms.validators import (  # type: ignore
    DataRequired,
    URL,
    Length,
    ValidationError
)
from yacut.constants import (
    ERROR_MESSAGES, MAX_CUSTOM_SHORT_ID_LENGTH, SHORT_ID_REGEX
)
from yacut.models import URLMap


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired('Обязательное поле'), URL()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=MAX_CUSTOM_SHORT_ID_LENGTH)]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data:
            if not re.match(SHORT_ID_REGEX, field.data):
                raise ValidationError(ERROR_MESSAGES['invalid_short_id'])
            if field.data == 'files':
                raise ValidationError(ERROR_MESSAGES['short_id_exists'])
            if URLMap.query.filter_by(short=field.data).first():
                raise ValidationError(ERROR_MESSAGES['short_id_exists'])


class FileForm(FlaskForm):
    files = MultipleFileField('Файлы', validators=[DataRequired()])
    submit = SubmitField('Загрузить')
