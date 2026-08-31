import asyncio
import io
import aiohttp
from flask import abort, render_template, redirect, url_for, send_file
import urllib
from yacut import app, db
from yacut.constants import ERROR_MESSAGES
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
        ERROR_MESSAGES['id_not_found']
    )
    original = url_map.original

    if original.startswith('/') or 'downloader.disk.yandex.ru' in original:
        try:
            if original.startswith('/'):
                download_link, filename = asyncio.run(
                    get_download_link(original)
                )
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
        except aiohttp.ClientError as e:
            abort(
                500,
                description=f'{ERROR_MESSAGES["download_error"]}: {str(e)}'
            )
        except ValueError as e:
            abort(
                500,
                description=f'{ERROR_MESSAGES["download_link_error"]}: '
                f'{str(e)}'
            )
        except Exception as e:
            abort(
                500,
                description=f'{ERROR_MESSAGES["unknown_download_error"]}: '
                f'{str(e)}'
            )

    return redirect(original)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = FileForm()
    results = []
    if form.validate_on_submit():
        files = form.files.data

        if not files or all(f.filename == '' for f in files):
            abort(400, description=ERROR_MESSAGES['no_files_selected'])

        async def process_files():
            tasks = [upload_file_to_disk(file_storage=f) for f in files]
            download_info = await asyncio.gather(*tasks)
            res = []
            for f, (file_path, display_name) in zip(files, download_info):
                short_id = get_unique_short_id()
                url_map = URLMap(original=file_path, short=short_id)
                db.session.add(url_map)
                db.session.commit()
                short_url = url_for(
                    'redirect_view', short_id=short_id, _external=True
                )
                res.append({'filename': display_name, 'short_url': short_url})
            return res

        try:
            results = asyncio.run(process_files())
        except aiohttp.ClientError as e:
            abort(
                500,
                description=f'{ERROR_MESSAGES["upload_error"]}: {str(e)}'
            )
        except Exception as e:
            abort(
                500,
                description=f'{ERROR_MESSAGES["unknown_upload_error"]}: {e}'
            )

    return render_template('files.html', form=form, results=results)
