from parser import download_images
from parser500px import scrape_500px_images # works fine
from parse_Flickr_API import download_flickr_images # works fine
from FLICKR_API_KEY import FLICKR_API_KEY # works fine

# URL для поиска изображений красной лисы
url_500px = "https://500px.com/search?q=red%20fox&type=photos&sort=relevance" # for scrape_500px_images only
url = "https://commons.wikimedia.org/w/index.php?search=red+fox&title=Special:MediaSearch&go=Go&type=image"



# Запуск парсинга изображений
download_flickr_images(FLICKR_API_KEY, "red fox", "test1", count=10) # works fine
scrape_500px_images(url=url, folder='./test2') # works fine
download_images(url=url, folder='test3') # works fine