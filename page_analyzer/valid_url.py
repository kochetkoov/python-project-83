import validators


def is_valid_url(url):
    """
    Проверяет, является ли переданная строка валидным URL.

    :param url: Строка для проверки.
    :type url: str
    :return: True, если строка является валидным URL, иначе False.
    :rtype: bool
    """
    return validators.url(url)
