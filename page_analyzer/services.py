from urllib.parse import urlparse

from .db import (
    add_check_url,
    add_url_to_db,
    get_all_urls,
    get_url_checks,
    get_url_detail,
    get_url_id,
    get_url_name,
)
from .valid_url import is_valid_url


def add_url_service(url):
    """
    Добавляет URL в базу данных.

    :param url: URL для добавления.
    :return: Кортеж (id, message), где:
    - id: ID нового URL (int) или None, если произошла ошибка.
    - message: Сообщение об успехе или ошибке (str).
    """
    error = is_valid_url(url)
    if error is not True:
        return None, "Некорректный URL"

    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    existing_url = get_url_id(normalized_url)
    if existing_url:
        return existing_url, "Страница уже существует"

    new_url_id = add_url_to_db(normalized_url)
    if not new_url_id:
        return None, "Не удалось добавить страницу"

    return new_url_id, "Страница успешно добавлена"


def get_urls_service():
    """
    Возвращает список всех URL.

    :return: Список URL или None, если произошла ошибка.
    """
    return get_all_urls()


def get_url_detail_service(url_id):
    """
    Возвращает детали URL и его проверки.

    :param url_id: ID URL.
    :return: Кортеж (url, checks), где:
    - url: Данные URL (tuple) или None, если URL не найден.
    - checks: Список проверок (list) или None, если произошла ошибка.
    """
    url = get_url_detail(url_id)
    if not url:
        return None, None

    checks = get_url_checks(url_id)
    return url, checks


def perform_url_check_service(url_id):
    """
    Выполняет проверку URL.

    :param url_id: ID URL.
    :return: True, если проверка успешна, иначе False.
    """
    url = get_url_name(url_id)
    if not url:
        return False

    return add_check_url(url, url_id)
