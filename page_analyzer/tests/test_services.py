import pytest


def test_add_url_service():
    # Тест на добавление валидного URL
    url_id, message = add_url_service("https://example.com")
    assert url_id is not None
    assert message == "Страница успешно добавлена"

    # Тест на добавление уже существующего URL
    url_id, message = add_url_service("https://example.com")
    assert url_id is not None
    assert message == "Страница уже существует"

    # Тест на добавление невалидного URL
    url_id, message = add_url_service("invalid-url")
    assert url_id is None
    assert message == "Некорректный URL"