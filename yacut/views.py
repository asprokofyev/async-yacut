import asyncio
import io
import aiohttp
from flask import abort, render_template, redirect, url_for, send_file
import urllib
from yacut import app, db
from yacut.forms import URLForm, FileForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.yandex_disk import get_download_link, upload_file_to_disk


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    short_url = None
    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data
        if custom_id:
            custom_id = custom_id.strip()
        if not custom_id:
            custom_id = get_unique_short_id()
        url_map = URLMap(original=original, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        short_url = url_for(
            'redirect_view', short_id=custom_id, _external=True
        )
    return render_template('index.html', form=form, short_url=short_url)


@app.route('/<short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404(
        'Указанный id не найден'
    )
    original = url_map.original

    if 'downloader.disk.yandex.ru' in original or '/disk/' in original:
        try:
            if original.startswith('/'):
                download_link = asyncio.run(get_download_link(original))
            else:
                download_link = original
                parsed = urllib.parse.urlparse(download_link)
                query_params = urllib.parse.parse_qs(parsed.query)
                filename = query_params.get(
                    'filename', [original.split('/')[-1]]
                )[0]

            async def fetch_file():
                async with aiohttp.ClientSession() as session:
                    async with session.get(download_link) as resp:
                        resp.raise_for_status()
                        return await resp.read()

            file_data = asyncio.run(fetch_file())

            return send_file(
                io.BytesIO(file_data),
                download_name=filename,
                as_attachment=True
            )
        except Exception as e:
            abort(500, description=f'Не удалось скачать файл: {str(e)}')

    return redirect(original)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = FileForm()
    results = []
    if form.validate_on_submit():
        files = form.files.data

        if not files or all(f.filename == '' for f in files):
            abort(400, description='Не выбрано ни одного файла')

        async def process_files():
            tasks = [upload_file_to_disk(file_storage=f) for f in files]
            download_info = await asyncio.gather(*tasks)
            res = []
            for f, (link, display_name) in zip(files, download_info):
                short_id = get_unique_short_id()
                url_map = URLMap(original=link, short=short_id)
                db.session.add(url_map)
                db.session.commit()
                short_url = url_for(
                    'redirect_view', short_id=short_id, _external=True
                )
                res.append({'filename': display_name, 'short_url': short_url})
            return res
        results = asyncio.run(process_files())

    return render_template('files.html', form=form, results=results)
