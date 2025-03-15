import os

import psycopg2
from dotenv import load_dotenv
from .web_parser import parse_webpage

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    """
    Устанавливает и возвращает соединение с базой данных.

    :return: Объект соединения с базой данных.
    :rtype: psycopg2.extensions.connection
    """
    return psycopg2.connect(DATABASE_URL)


def add_url_to_db(url):
    """
    Добавляет URL в базу данных.

    :param url: URL для добавления.
    :type url: str
    :return: ID новой записи или None, если произошла ошибка.
    :rtype: int or None
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''INSERT INTO urls (name) VALUES (%s)''', (url,))
                new_url_id = cur.fetchone()[0]
                conn.commit()
                return new_url_id
    except Exception as e:
        print(f'Ошибка при добавлении записи: {e}')
        return None


def get_url_id(url):
    """
    Возвращает ID записи, если URL существует в базе данных.

    :param url: URL для поиска.
    :type url: str
    :return: ID записи или None, если URL не найден.
    :rtype: int or None
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT id FROM urls WHERE name = %s', (url,))
                result = cur.fetchone()
                return result[0] if result else None  # Возвращаем ID или None
    except Exception as e:
        print(f'Ошибка при выполнении запроса: {e}')
        return None


def get_all_urls():
    """
    Возвращает список всех URL с их последней проверкой (если есть).

    :return: Список кортежей с данными URL или None, если произошла ошибка.
    :rtype: list of tuples or None
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
            SELECT urls.id, urls.name, urls.created_at,
            MAX(url_checks.created_at), MAX(url_checks.status_code)
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            GROUP BY urls.id
            ORDER BY urls.id DESC
        """)
                urls = cur.fetchall()
                return urls
    except Exception as e:
        print(f'Возникла ошибка: {e}')
        return None


def get_url_detail(id):
    """
    Возвращает детали URL по его ID.

    :param id: ID URL для поиска.
    :type id: int
    :return: Кортеж с данными URL или None, если произошла ошибка.
    :rtype: tuple or None
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM urls WHERE id = %s;', (id,))
                url = cur.fetchone()
                return url
    except Exception as e:
        print(f'Возникла ошибка: {e}')
        return None


def get_url_checks(id):
    """
    Возвращает список проверок для указанного URL.

    :param id: ID URL для поиска проверок
    :type id: int
    :return: Список кортежей с данными проверок или None, если произошла ошибка
    :rtype: list of tuples or None
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
                ''', (id,))
                checks = cur.fetchall()
                return checks
    except Exception as e:
        print(f'Возникла ошибка: {e}')
        return None


def get_url_name(id):
    """
    Возвращает имя URL по его ID.

    :param id: ID URL для поиска.
    :type id: int
    :return: Имя URL или None, если произошла ошибка.
    :rtype: str or None
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT name FROM urls WHERE id = %s', (id,))
                result = cur.fetchone()
                return result[0] if result else None  # Возвращаем ID или None
    except Exception as e:
        print(f'Ошибка при выполнении запроса: {e}')
        return None


def add_check_url(url, id):
    """
    Добавляет проверку URL в базу данных.

    :param url: URL для проверки.
    :type url: str
    :param id: ID URL в базе данных.
    :type id: int
    :return: True, если проверка успешно добавлена, иначе None.
    :rtype: bool or None
    """
    try:
        h1, title, description, status_code = parse_webpage(url)
        if status_code == 200:
            status_check = True
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('''INSERT INTO url_checks
                        (url_id, status_code, h1,
                        title, description, created_at)
                        VALUES
                        (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                        ''', (id, status_code, h1, title, description))
                    conn.commit()
                    return status_check

    except Exception as e:
        print(f'Возникла ошибка: {e}')
        return None
