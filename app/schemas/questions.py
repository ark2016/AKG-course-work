from pydantic import BaseModel
from typing import Optional


# Модель запроса для download_images
class DownloadImagesRequest(BaseModel):
    url: str = "https://commons.wikimedia.org/w/index.php?search=red+fox&title=Special:MediaSearch&go=Go&type=image"
    folder: Optional[str] = "test"


# Модель запроса для scrape_500px_images
class Scrape500pxImagesRequest(BaseModel):
    url: str = "https://500px.com/search?q=red%20fox&type=photos&sort=relevance"
    folder: Optional[str] = "test"
