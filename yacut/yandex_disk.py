import urllib.parse
import aiohttp  # type: ignore
from yacut import app

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
DISK_TOKEN = app.config['DISK_TOKEN']

AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}


async def get_upload_link(filename: str, overwrite: bool = True) -> str:
    params = {
        'path': f'/{filename}',
        'overwrite': str(overwrite).lower()
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=REQUEST_UPLOAD_URL, headers=AUTH_HEADERS, params=params
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data['href']


async def upload_file_to_url(upload_url: str, file_data: bytes) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.put(url=upload_url, data=file_data) as resp:
            resp.raise_for_status()
            location = resp.headers['Location']
            location = urllib.parse.unquote(location)
            location = location.replace('/disk', '')
            return location


async def get_download_link(file_path: str) -> tuple[str, str]:
    params = {'path': file_path}
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=DOWNLOAD_LINK_URL, headers=AUTH_HEADERS, params=params
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            download_link = data['href']

            parsed = urllib.parse.urlparse(download_link)
            query_params = urllib.parse.parse_qs(parsed.query)
            if 'filename' in query_params:
                filename = query_params['filename'][0]
            else:
                filename = file_path.split('/')[-1]

            return download_link, filename


async def upload_file_to_disk(file_storage) -> tuple[str, str]:
    upload_url = await get_upload_link(filename=file_storage.filename)
    file_data = file_storage.read()
    file_path = await upload_file_to_url(
        upload_url=upload_url, file_data=file_data
    )
    download_link, _ = await get_download_link(file_path)
    return download_link, file_storage.filename
