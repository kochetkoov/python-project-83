import os
from flask import Flask, render_template, request, redirect, flash, url_for
from dotenv import load_dotenv
import requests
import psycopg2
from bs4 import BeautifulSoup


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')


# Проверка на валидность URL адреса
def is_valid_url(url):
    return url.startswith('http://') or url.startswith('https://')


# Подключение к базе данных
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(f'Возникла ошибка: {str(e)}')
    return conn


# Отображение главной страницы
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']

        if len(url) > 255 or not is_valid_url(url):
            flash('Некорректный URL', 'danger')
            return redirect(url_for('home'))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM urls WHERE name = %s', (url,))
        existing_url = cur.fetchone()

        if existing_url:
            flash('Страница уже существует', 'info')
            return redirect(f'/urls/{existing_url[0]}')
        else:
            cur.execute('INSERT INTO urls (name) VALUES (%s)', (url,))
            conn.commit()

            cur.execute('SELECT id FROM urls WHERE name = %s', (url,))
            index = cur.fetchone()[0]

            cur.close()
            conn.close()

            flash('Страница успешно добавлена', 'success')
            return redirect(f'/urls/{index}')

    return render_template('home.html')


# Страница всех URL
@app.route('/urls', methods=['GET', 'POST'])
def get_urls():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT urls.id, urls.name, urls.created_at,
        MAX(url_checks.created_at), MAX(url_checks.status_code)
        FROM urls
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
        GROUP BY urls.id
        ORDER BY urls.id DESC
    """)
    urls = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('urls.html', urls=urls)


# Страница конкретного URL
@app.route('/urls/<int:id>')
def url_detail(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM urls WHERE id = %s;', (id,))
    url = cur.fetchone()

    if url is None:
        return f'URL с {id} не найден', 404

    cur.execute('''SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
                ''', (id,))
    checks = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('url_detail.html', url=url, checks=checks)


# Страница с проверкой URL на SEO пригодность
@app.route('/urls/<int:id>/checks')
def check_url(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT name FROM urls WHERE id = %s', (id,))
    url = cur.fetchone()[0]

    if url is None:
        flash('URL не найден', 'danger')
        return redirect('/urls')

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        h1 = soup.find('h1').get_text() if soup.find('h1') else None
        title = soup.find('title').get_text() if soup.find('title') else None
        description = (
                soup.find('meta', attrs={'name': 'description'})['content']
                if soup.find('meta', attrs={'name': 'description'})
                else None
        )
        status_code = response.status_code
        if int(status_code) == 200:
            cur.execute('''INSERT INTO url_checks
                        (url_id, status_code, h1,
                        title, description, created_at)
                        VALUES
                        (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                        ''', (id, status_code, h1, title, description))
            conn.commit()
            flash('Страница успешно проверена', 'success')
        else:
            flash('Произошла ошибка при проверке', 'danger')
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('url_detail', id=id))


if __name__ == '__main__':
    app.run()
