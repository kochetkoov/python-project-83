import os

from flask import Flask, flash, redirect, render_template, request, url_for

from .services import (
    add_url_service,
    get_url_detail_service,
    get_urls_service,
    perform_url_check_service,
)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Обрабатывает главную страницу и добавление нового URL.

    :return: Шаблон home.html или перенаправление на страницу URL.
    """
    if request.method == 'POST':
        url = request.form['url']
        url_id, message = add_url_service(url)

        if not url_id:
            flash(message, 'danger')
            return redirect(url_for('home'))

        flash(message, 'success')
        return redirect(f'/urls/{url_id}')

    return render_template('home.html')


@app.route('/urls', methods=['GET', 'POST'])
def get_urls():
    """
    Отображает список всех URL.

    :return: Шаблон urls.html или перенаправление на главную страницу.
    """
    urls = get_urls_service()
    if not urls:
        flash('Не получилось выполнить запрос', 'danger')
        return redirect('/')
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
        return redirect('/urls')

    if checks is None:
        flash('Не удалось получить данные о проверках', 'danger')
        return redirect('/')

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
