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


# Модель запроса для download_flickr_images
class DownloadFlickrImagesRequest(BaseModel):
    search_text: str = "red fox"
    folder: Optional[str] = "test"
    count: Optional[int] = 100


# Модель запроса для создания датасета
class CreateDatasetRequest(BaseModel):
    source_dir: str
    output_dir: str


class PredictionRequest(BaseModel):
    image_path: str
