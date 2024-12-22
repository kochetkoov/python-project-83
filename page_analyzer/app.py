from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Получаем строку подключения из переменной окружения
DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Функция для подключения к базе данных
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']

        # Проверка валидности URL
        if len(url) > 255 or not url.startswith('http'):
            flash('Неверный URL! Он должен быть валидным и не превышать 255 символов.', 'danger')
            return redirect(url_for('home'))

        # Сохраняем URL в базе данных
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO urls (name) VALUES (%s)', (url,))
        conn.commit()
        cur.close()
        conn.close()

        flash('URL успешно добавлен!', 'success')
        return redirect(url_for('home'))

    return render_template('home.html')

@app.route('/urls')
def urls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM urls ORDER BY created_at DESC')
    urls = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('urls.html', urls=urls)

@app.route('/urls/<int:url_id>')
def url_detail(url_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
    url = cur.fetchone()
    cur.close()
    conn.close()

    if url is None:
        flash('URL не найден!', 'danger')
        return redirect(url_for('urls'))

    return render_template('url_detail.html', url=url)

if __name__ == '__main__':
    app.run(debug=True)
