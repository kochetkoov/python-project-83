import os

from flask import Flask, flash, redirect, render_template, request, url_for

from .valid_url import is_valid_url
from .db import (
    get_url_id,
    add_url_to_db,
    get_all_urls,
    get_url_detail,
    get_url_checks,
    get_url_name,
    add_check_url
    )

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Отображает главную страницу и обрабатывает добавление нового URL.

    Если метод запроса GET:
        - Отображает главную страницу (шаблон home.html).

    Если метод запроса POST:
        - Получает URL из формы.
        - Проверяет валидность URL.
        - Если URL невалидный, выводит сообщение об ошибке
        и перенаправляет на главную страницу.
        - Если URL валидный, проверяет, существует ли он в базе данных.
        - Если URL уже существует, выводит сообщение
        и перенаправляет на страницу этого URL.
        - Если URL новый, добавляет его в базу данных
        и перенаправляет на страницу нового URL.

    :return:
        - При GET: Шаблон home.html.
        - При POST: Перенаправление на страницу URL (нового или существующего)
        или на главную страницу в случае ошибки.
    """
    if request.method == 'POST':
        url = request.form['url']

        valid_url = is_valid_url(url)
        if not valid_url:
            flash('Некорректный URL', 'danger')
            return redirect(url_for('home'))

        existing_url = get_url_id(url)

        if existing_url:
            flash('Страница уже существует', 'info')
            return redirect(f'/urls/{existing_url}')
        else:
            new_url = add_url_to_db(url)
            if not new_url:
                flash('Не удалось добавить страницу', 'danger')
                return redirect(url_for('home'))


            flash('Страница успешно добавлена', 'success')
            return redirect(f'/urls/{new_url}')

    return render_template('home.html')


@app.route('/urls', methods=['GET', 'POST'])
def get_urls():
    """
    Отображает страницу со списком всех URL.

    :return: Шаблон urls.html с данными URL или
    перенаправление на главную страницу в случае ошибки.
    """
    urls = get_all_urls()
    if not urls:
        flash('Не получилось выполнить запрос', 'danger')
        return redirect('/')
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def url_detail(id):
    """
    Отображает страницу с деталями конкретного URL и его проверками.

    :param id: ID URL для отображения.
    :return: Шаблон url_detail.html с данными URL и проверками или сообщение об ошибке.
    """
    url = get_url_detail(id)

    if url is None:
        flash('URL не найден', 'danger')
        return redirect('/urls')

    checks = get_url_checks(id)
    if checks is None:
        flash('Не удалось получить данные о проверках', 'danger')
        return redirect('/')
    return render_template('url_detail.html', url=url, checks=checks)



@app.route('/urls/<int:id>/checks')
def check_url(id):
    """
    Проверяет URL на SEO-пригодность и добавляет проверку в базу данных.

    :param id: ID URL для проверки.
    :return: Перенаправление на страницу с деталями URL или на список URL в случае ошибки.
    """
    url = get_url_name(id)
    if url is None:
        flash('URL не найден', 'danger')
        return redirect('/urls')

    status_check = add_check_url(url, id)
    if status_check:
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('url_detail', id=id))
    else:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect('/urls')  #


if __name__ == '__main__':
    app.run()
