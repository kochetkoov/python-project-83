from .db import (
    add_check_url,
    get_all_urls,
    get_url_checks,
    get_url_detail,
    get_url_name,
)


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
