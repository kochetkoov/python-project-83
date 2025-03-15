import requests
from bs4 import BeautifulSoup


def parse_webpage(url):
    """
    Парсит веб-страницу и извлекает данные:
    h1, title, description и status_code.

    :param url: URL веб-страницы для парсинга.
    :return:
    - h1: Заголовок h1.
    - title: Заголовок страницы.
    - description: Мета-описание.
    - status_code: Код статуса HTTP.
    """
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
        return h1, title, description, status_code

    except Exception as e:
        print(f'Ошибка при запросе к {url}: {e}')
        return None
