import validators


def is_valid_url(url):
    if len(url) > 255:
        return 'URL превышает 255 символов'
    elif validators.url(url) is not True:
        return 'Некорректный URL'
