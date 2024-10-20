import os
import requests

# Ваш Flickr API ключ
FLICKR_API_KEY =

# URL для запроса к API Flickr
FLICKR_API_URL = "https://www.flickr.com/services/rest/"

# Параметры запроса к Flickr API
PARAMS = {
    "method": "flickr.photos.search",
    "api_key": FLICKR_API_KEY,
    "text": "red fox",  # Поисковый запрос
    "content_type": 1,  # Только фотографии
    "media": "photos",
    "sort": "relevance",
    "per_page": 500,  # Количество результатов на странице
    "format": "json",
    "nojsoncallback": 1  # Чтобы получить чистый JSON
}


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
def scrape_flickr_images(params):
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
        download_image(image_url, image_name=f"red_fox_{i}")


# Запускаем парсинг изображений с Flickr
scrape_flickr_images(PARAMS)