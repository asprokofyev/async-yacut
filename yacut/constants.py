DEFAULT_SHORT_ID_LENGTH = 6

MAX_CUSTOM_SHORT_ID_LENGTH = 16

MAX_ORIGINAL_URL_LENGTH = 1024

SHORT_ID_REGEX = r'^[A-Za-z0-9]+$'

RESERVED_NAMES = {'files'}

ERROR_MESSAGES = {
    'invalid_short_id': 'Указано недопустимое имя для короткой ссылки',
    'short_id_exists': 'Предложенный вариант короткой ссылки уже существует.',
    'missing_body': 'Отсутствует тело запроса',
    'missing_url': '"url" является обязательным полем!',
    'id_not_found': 'Указанный id не найден',
    'page_not_found': 'Страница не найдена',
    'no_files_selected': 'Не выбрано ни одного файла',
    'download_error': 'Не удалось скачать файл',
    'download_link_error': 'Некорректная ссылка на файл',
    'unknown_download_error': 'Неожиданная ошибка при скачивании файла',
    'upload_error': 'Ошибка при загрузке файлов на Яндекс.Диск',
    'unknown_upload_error': 'Неожиданная ошибка при загрузке файлов',
    'forbidden': 'Доступ запрещён',
    'internal_error': 'Внутренняя ошибка сервера',
    'bad_request': 'Некорректный запрос',
}

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
UPLOAD_DIR = '/'
