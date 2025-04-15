import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .db import add_url_to_db, get_url_id
from .services import (
    get_url_detail_service,
    get_urls_service,
    perform_url_check_service,
)
from .valid_url import is_valid_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def home():
    return render_template('home.html')


@app.post('/urls')
def add_url():
    url = request.form.get('url')

    error = is_valid_url(url)
    if error:
        flash(f'{error}', 'danger')
        return render_template('home.html', url=url), 422

    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    existing_url = get_url_id(normalized_url)
    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('url_detail', id=existing_url))

    new_url_id = add_url_to_db(normalized_url)
    if not new_url_id:
        flash('Не удалось добавить страницу', 'danger')
        return render_template('home.html', url=url), 500

        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('url_detail', id=new_url_id))

    return render_template('home.html')


@app.get('/urls')
def get_urls():
    """
    Отображает список всех URL.

    :return: Шаблон urls.html или перенаправление на главную страницу.
    """
    urls = get_urls_service()
    if not urls:
        flash('Не получилось выполнить запрос', 'danger')
        return render_template('home.html')
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def url_detail(id):
    """
    Отображает детали URL и его проверки.

    :param id: ID URL.
    :return: Шаблон url_detail.html или перенаправление на список URL.
    """
    url, checks = get_url_detail_service(id)

    if not url:
        flash('URL не найден', 'danger')
        return render_template('urls.html')

    if checks is None:
        flash('Не удалось получить данные о проверках', 'danger')
        return render_template('home.html')

    return render_template('url_detail.html', url=url, checks=checks)


@app.route('/urls/<int:id>/checks')
def check_url(id):
    """
    Выполняет проверку URL.

    :param id: ID URL.
    :return: Перенаправление на страницу URL.
    """
    if perform_url_check_service(id):
        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('url_detail', id=id))


if __name__ == '__main__':
    app.run()
