from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()   # Загружаем переменные окружения

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
# Устанавливаем SECRET KEY


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
