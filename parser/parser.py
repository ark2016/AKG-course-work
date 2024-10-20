import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL для поиска изображений красной лисы на Wikimedia Commons
url = "https://500px.com/search?q=red%20fox&type=photos&sort=relevance"

# Заголовки, чтобы эмулировать запросы от браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


# Функция для парсинга изображений
def download_images(url, folder='images'):
    # Создаем папку для скачанных изображений
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Получаем страницу
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Проверка на успешность запроса

    # Парсим HTML с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем теги <img> с картинками
    images = soup.find_all('img')

    # Скачиваем каждое изображение
    for i, img in enumerate(images):
        img_url = img.get('src')
        if img_url:
            # Преобразуем относительные ссылки в абсолютные
            img_url = urljoin(url, img_url)

            # Получаем расширение файла
            ext = img_url.split('.')[-1]

            try:
                # Скачиваем изображение
                img_data = requests.get(img_url).content
                # Сохраняем изображение в папку
                img_name = os.path.join(folder, f'red_fox_{i}.{ext}')
                with open(img_name, 'wb') as f:
                    f.write(img_data)
                print(f'Изображение сохранено: {img_name}')
            except Exception as e:
                print(f'Ошибка при скачивании изображения {img_url}: {e}')


# Запускаем парсинг
download_images(url, folder='500px')