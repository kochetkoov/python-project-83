import validators


def is_valid_url(url):
    if len(url) > 255:
        return False
    return validators.url(url)
