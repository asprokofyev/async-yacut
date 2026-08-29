import re
from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField, SubmitField, MultipleFileField  # type: ignore
from wtforms.validators import (  # type: ignore
    DataRequired,
    URL,
    Length,
    ValidationError
)
from yacut.models import URLMap


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(), URL()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=16)]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data:
            if not re.match(r'^[A-Za-z0-9]+$', field.data):
                raise ValidationError(
                    'Указано недопустимое имя для короткой ссылки'
                )
            if field.data == 'files':
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
            if URLMap.query.filter_by(short=field.data).first():
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )


class FileForm(FlaskForm):
    files = MultipleFileField('Файлы', validators=[DataRequired()])
    submit = SubmitField('Загрузить')
