import os
from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
import psycopg2


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')

try:
    conn = psycopg2.connect('postgresql://janedoe:mypassword@localhost:5432/mydb')
    cur = conn.cursor()
except:
    print('Возникла ошибка при подключении')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']

        if len(url) > 255 or not is_valid_url(url):
            flash('URL должен быть валидным', 'error')
            return redirect('/')
        try:
            cur.execute("INSERT INTO urls (name) VALUES (%s)", (url,))
            conn.commit()
            flash('URL успешно добавлен', 'success')
            return redirect('/urls')
        except Exception as e:
            flash(f'Ошибка при добавлении URL: {str(e)}', 'error')
            print(f'Error: {str(e)}')
            conn.rollback()
            return redirect('/')

    return render_template('home.html')

def is_valid_url(url):
    return url.startswith('http://') or url.startswith('https://')


@app.route('/urls')
def get_urls():
    cur.execute('SELECT * FROM urls ORDER BY created_at DESC')
    urls = cur.fetchall()
    return render_template('urls.html', urls=urls)


if __name__ == '__main__':
    app.run()
