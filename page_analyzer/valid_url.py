import validators


def is_valid_url(url):
    """Проверка на валидность URL адреса"""
    return validators.url(url)

