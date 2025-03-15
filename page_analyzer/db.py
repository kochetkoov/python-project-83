import os

import psycopg2
from dotenv import load_dotenv
from .web_parser import parse_webpage

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    """Подключение к базе данных"""
    return psycopg2.connect(DATABASE_URL)


def add_url_to_db(url):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = cur.execute('INSERT INTO urls (name) VALUES (%s)',
                                    (url,))
                new_url_id = cur.fetchone()[0]
                conn.commit()
                return new_url_id
    except Exception as e:
        print(f'Ошибка при добавлении записи: {e}')
        return None

def get_url_id(url):
    """Возвращает ID записи, если URL существует в базе данных, иначе None."""
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
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                '''SELECT id, status_code, h1, title, description, created_at
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
