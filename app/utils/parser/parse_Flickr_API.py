import os
import requests
from app.utils.parser.FLICKR_API_KEY import FLICKR_API_KEY

# URL для запроса к API Flickr
FLICKR_API_URL = "https://www.flickr.com/services/rest/"

# Функция для скачивания изображения
def download_image(url, folder='flickr_images', image_name=None):
    if not os.path.exists(folder):
        os.makedirs(folder)

    try:
        img_data = requests.get(url).content
        if image_name:
            file_path = os.path.join(folder, f"{image_name}.jpg")
        else:
            file_path = os.path.join(folder, url.split('/')[-1])

        with open(file_path, 'wb') as f:
            f.write(img_data)
        print(f"Изображение сохранено: {file_path}")
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")

# Функция для парсинга изображений с Flickr API
def download_flickr_images(api_key=FLICKR_API_KEY, search_text="red fox", folder="test", count=500):
    params = {
        "method": "flickr.photos.search",
        "api_key": api_key,
        "text": search_text,  # Поисковый запрос
        "content_type": 1,  # Только фотографии
        "media": "photos",
        "sort": "relevance",
        "per_page": count,  # Количество результатов на странице
        "format": "json",
        "nojsoncallback": 1  # Чтобы получить чистый JSON
    }

    response = requests.get(FLICKR_API_URL, params=params)
    response.raise_for_status()

    # Получаем JSON-ответ
    data = response.json()

    if 'photos' not in data:
        print("Не удалось найти изображения.")
        return

    # Получаем список фотографий
    photos = data['photos']['photo']

    # Проходим по каждой фотографии
    for i, photo in enumerate(photos):
        # Конструируем URL для получения изображения
        photo_id = photo['id']
        farm_id = photo['farm']
        server_id = photo['server']
        secret = photo['secret']
        image_url = f"https://farm{farm_id}.staticflickr.com/{server_id}/{photo_id}_{secret}.jpg"

        # Скачиваем изображение
        download_image(image_url, folder=folder, image_name=f"{search_text}_{i}")