import os
import requests

# URL API Wikimedia Commons
API_URL = "https://commons.wikimedia.org/w/api.php"

# Параметры для запроса к API
PARAMS = {
    "action": "query",
    "format": "json",
    "generator": "search",
    "gsrsearch": "red fox",  # Поисковый запрос
    "gsrlimit": 200,  # Количество результатов (измените по необходимости)
    "prop": "imageinfo",
    "iiprop": "url",  # Получаем URL изображений
    # "iiurlwidth": 500,  # Опционально: задаем ширину изображения
}


# Функция для скачивания изображений
def download_images_from_commons(params, save_folder="commons_images"):
    # Создаем папку для изображений, если она не существует
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Выполняем запрос к API
    response = requests.get(API_URL, params=params)
    response.raise_for_status()

    # Парсим JSON-ответ от API
    data = response.json()

    # Проверяем, есть ли данные
    if "query" not in data:
        print("Изображения не найдены.")
        return

    # Получаем страницы с изображениями
    pages = data["query"]["pages"]

    # Проходим по каждой странице и сохраняем изображения
    for page_id, page_data in pages.items():
        if "imageinfo" in page_data:
            image_url = page_data["imageinfo"][0]["url"]
            image_title = page_data["title"].replace("File:", "").replace(" ", "_")
            image_extension = image_url.split(".")[-1]

            try:
                print(f"Скачивание изображения: {image_title}")
                img_data = requests.get(image_url).content
                with open(os.path.join(save_folder, f"{image_title}.{image_extension}"), 'wb') as f:
                    f.write(img_data)
                print(f"Изображение сохранено: {image_title}.{image_extension}")
            except Exception as e:
                print(f"Ошибка при скачивании {image_title}: {e}")
        else:
            print(f"Изображение не найдено для страницы {page_data.get('title', 'Unknown')}")


# Запускаем функцию для скачивания изображений
download_images_from_commons(PARAMS)