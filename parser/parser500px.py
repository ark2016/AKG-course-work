import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Функция для скачивания изображений
def download_image(url, folder='500px_images_v2', image_name=None):
    if not os.path.exists(folder):
        os.makedirs(folder)

    try:
        img_data = requests.get(url).content
        if image_name:
            file_path = os.path.join(folder, f"{image_name}.jpg")
        else:
            file_path = os.path.join(folder, url.split("/")[-1])

        with open(file_path, 'wb') as f:
            f.write(img_data)
        print(f"Изображение сохранено: {file_path}")
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")


# Настройки для Selenium
def setup_driver():
    # Настройка Chrome для запуска через WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск без открытия окна браузера
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Устанавливаем драйвер с помощью webdriver_manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# Функция для парсинга изображений с сайта 500px
def scrape_500px_images(search_url, scroll_pause_time=2, num_scrolls=15):
    driver = setup_driver()
    driver.get(search_url)

    # Прокручиваем страницу вниз несколько раз, чтобы загрузить больше изображений
    for _ in range(num_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

    # Ищем все элементы изображения на странице
    image_elements = driver.find_elements(By.CSS_SELECTOR, "img")

    # Фильтруем изображения (получаем только ссылки на полноразмерные изображения)
    image_urls = []
    for img in image_elements:
        src = img.get_attribute('src')
        if src and "500px" in src:
            image_urls.append(src)

    driver.quit()  # Закрываем браузер после завершения

    # Скачиваем каждое изображение
    for idx, url in enumerate(image_urls):
        download_image(url, image_name=f"red_fox_{idx}")


# URL для поиска изображений лисы
search_url = "https://500px.com/search?q=red%20fox&type=photos&sort=relevance"

# Запуск парсинга изображений
scrape_500px_images(search_url)